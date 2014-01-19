""" Server module for the grading application """

from flask import (Flask, send_from_directory, render_template, request,
                   session, redirect, send_file)
from werkzeug import secure_filename
from database import db_session
import database
import ldap
import os
import test_data
import sys
import auth
import datetime

# Add the current folder to the pythonpath
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

# create the application
app = Flask(__name__)

# Currently, we want to enable debugging mode
app.debug = True

# Create a private key for cookie encryption/decryption
app.secret_key = os.urandom(8).encode('hex')

# allowed upload extensions, currently only allows zip
ALLOWED_EXTENSIONS = ['zip']

def extension_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.before_request
def before_request():
    # if the request is to login, or get assets like css, let them through
    if request.path == '/login' or request.path[0:7] == '/assets':
        return
    # if the user has logged in, continue the request normally
    elif 'net_id' in session:
        return
    # otherwise, redirect to the login page
    else:
        return redirect('/login')


@app.route('/')
def index_route():
    sub = database.Student.get_submitted_assignments(session['net_id'])
    unsub = database.Student.get_unsubmitted_assignments(session['net_id'])
    return render_template('index.html',
                           page_title="Home",
                           submitted_assignments=sub,
                           unsubmitted_assignments=unsub
                           )


@app.route('/assignment/<int:id>')
def assignment_route(id):
    # get the requested assignment
    assignment = database.Assignment.get_active_assignment_by_id(id)
    # Get the submissions
    submissions = database.Assignment.get_assignment_submissions(session['net_id'], id)
    # figure out if this assignment was finalized
    is_final = database.Assignment.check_assignment_completed(session['net_id'], id)
    # get the resources from the assignment
    resources = database.Assignment.get_assignment_resources(id)
    # display assignment page
    return render_template('assignment.html',
                           assignment=assignment,
                           submissions=submissions,
                           resources=resources,
                           is_final=is_final,
                           page_title='Assignment ' + str(id))

@app.route('/assignment/<int:id>/submit', methods=['POST'])
def assignment_submit_route(id):
    if request.method == 'POST':
        archive = request.files['archive']
        if not archive:
            return 'No file chosen', 400
        if not extension_allowed(archive.filename):
            return 'Wrong file type chosen, you need to upload a zip', 400
        # check if this is the final submission
        is_final = True if 'is_final' in request.form else False
        # create new submission
        sub_id  = database.Submission.create_submission(id, session['net_id'], datetime.datetime.now(), is_final)
        #create the assignment directory structure
        student_directory = os.path.join(current_path,
                                 '..',
                                 'submissions',
                                 'assignment' + str(id),
                                 session['net_id'],
                                 str(sub_id)
                    )
        if not os.path.exists(student_directory):
            os.makedirs(student_directory)
        filename = secure_filename(archive.filename)
        archive.save(os.path.join(student_directory, filename))
        return 'Success', 200

@app.route('/resource/<int:id>')
def get_resource(id):
    resource = db_session.query(database.Resource).get(id)
    assignment = 'assignment' + str(resource.assignment.id)
    resource_filename = resource.filename
    path = os.path.join(current_path,
                        '..',
                        'assignments',
                        assignment,
                        'resources'
                        )
    return send_file(path + '/' + resource_filename,
                     as_attachment=True,
                     attachment_filename=resource_filename)

@app.route('/submission/<int:id>')
def test_route(id):
    test_output = open(current_path + '/sample_test.txt').read()
    print test_output
    test = {
        "id": 5,
        "test_output": test_output
    }
    return render_template('submission.html', test=test)


@app.route('/logout')
def logout_route():
    del session['net_id']
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    # Just render the template
    if request.method == 'GET':
        return render_template('login.html')
    # if they're trying to login
    else:
        username = None
        password = None
        try:
            username = request.form['username']
        except KeyError:
            return render_template('login.html', error="Username required")
        try:
            password = request.form['password']
        except KeyError:
            return render_template('login.html', error="Password required")
        if not auth.auth_user(username, password):
            return render_template('login.html', error="Invalid credentials")
        session['net_id'] = username
        return redirect('/')


# Serves static resources like css, js, images, etc.
@app.route('/assets/<path:resource>')
def serve_static_resource(resource):
    asset_path = current_path + '/static/assets/'
    # Return the static file
    return send_from_directory(asset_path, resource)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    database.test_data()
    app.run("0.0.0.0", 8000)
