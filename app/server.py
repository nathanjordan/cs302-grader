""" Server module for the grading application """

from flask import (Flask, send_from_directory, render_template, request,
                   session, redirect)
import database
import ldap
import os

app = Flask(__name__)

app.debug = True

app.secret_key = os.urandom(8).encode('hex')

current_path = os.path.dirname(os.path.realpath(__file__))


@app.before_request
def before_request():
    if request.path == '/login' or request.path[0:7] == '/assets':
        return
    elif 'username' in session:
        return
    else:
        return redirect('/login')


@app.route('/')
def index_route():
    return render_template('index.html')


@app.route('/assignment/<int:id>')
def assignment_route(id):
    assignment = {
        "id": 1,
        "name": "Stacks"
    }
    return render_template('assignment.html', assignment=assignment)


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
    del session['username']
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = None
        password = None
        try:
            username = request.form['username']
        except KeyError:
            return 'Username required', 400
        try:
            password = request.form['password']
        except KeyError:
            return 'Password required', 400
        # TODO: Authenticate with ldap here...
        pass
        # TODO: Setup session here
        session['username'] = username
        return redirect('/')


# Serves static resources like css, js, images, etc.
@app.route('/assets/<path:resource>')
def serve_static_resource(resource):
    asset_path = current_path + '/static/assets/'
    # Return the static file
    return send_from_directory(asset_path, resource)

if __name__ == '__main__':
    app.run("0.0.0.0", 8000)
