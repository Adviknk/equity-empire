from flask import Flask, render_template, request, redirect, session
from helper import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
@app.route("/home")
@app.route("/home/<username>")
def home(username=''):
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html', username='')


@app.route("/explore")
@app.route("/explore/<username>")
def explore(username=''):
    if 'username' in session:
        return render_template('explore.html', username=session['username'])
    else:
        return render_template('explore.html', username='')


@app.route("/leagues")
@app.route("/leagues/<username>")
def leagues(username=''):
    if 'username' in session:
        return render_template('league-home.html', username=session['username'])
    else:
        return redirect('/login')


@app.route("/account")
@app.route("/account/<username>")
def account(username=''):
    if 'username' in session:
        return render_template('account.html', username=session['username'])
    else:
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("log-in.html")

    if request.method == "POST":
        user_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if user_name == '':
            return render_template("login-error.html", error='username is invalid')

        session['username'] = user_name
        return redirect('/account/' + user_name)


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")

    if request.method == "POST":
        first = request.form.get('first')
        last = request.form.get('last')
        user_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if user_name == '':
            return render_template("signup-error.html", error='username is invalid')

        session['username'] = user_name

        return redirect('/account' + user_name)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
