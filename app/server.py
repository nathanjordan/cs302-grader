from flask import Flask, send_from_directory, render_template
import ldap

app = Flask(__name__)


@app.route('/')
def index_route():
    return render_template('login.html')


# Serves static resources like css, js, images, etc.
@app.route('/assets/<path:resource>')
def serveStaticResource(resource):
    # Return the static file
    return send_from_directory('static/assets/', resource)

if __name__ == '__main__':
    app.run("0.0.0.0", 8000)
