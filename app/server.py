""" Server module for the grading application """

from flask import (Flask, send_from_directory, render_template, request,
                   session, redirect)
import database
import ldap
import os
import test_data
import sys
import auth

# Add the current folder to the pythonpath
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

app = Flask(__name__)

app.debug = True

app.secret_key = os.urandom(8).encode('hex')

current_path = os.path.dirname(os.path.realpath(__file__))


@app.before_request
def before_request():
    if request.path == '/login' or request.path[0:7] == '/assets':
        return
    elif 'net_id' in session:
        return
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
    assignment = {
        "id": 1,
        "name": "Stacks"
    }
    return render_template('assignment.html',
                           assignment=assignment,
                           page_title="Assignment " + str(id))


@app.route('/test/<int:id>')
def test_route(id):
    test_output = open(current_path + '/sample_test.txt').read()
    print test_output
    test = {
        "id": 5,
        "test_output": test_output
    }
    return render_template('test.html', test=test)


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

if __name__ == '__main__':
    app.run("0.0.0.0", 8000)
