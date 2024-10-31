from flask import Flask, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from datetime import timedelta
from supporting_functions import *


app = Flask(__name__)
app.secret_key = '#FrontInnovation1234567890#'  # Set to a unique, secret value
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route("/") # Login route
def index():
    session.pop('user', None)
    return app.send_static_file("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_credentials(username, password):
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route("/dashboard") # Dashboard route
def dashboard():
    print('username')
    print(session)
    if 'username' in session:
        # The user is logged in
        return app.send_static_file("dashboard.html")
    else:
        return redirect(url_for("index"))
    
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    print("POPPED: ", session)
    return redirect(url_for('index'))

@app.route("/getdata")
def getdata():
    selskapsnavn = request.args.get("data")
    return 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")
    #app.run(ssl_context='adhoc')
