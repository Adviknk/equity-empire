from flask import Flask, render_template, request, redirect
from helper import *

app = Flask(__name__)

signedIn = False


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/account")
def account():
    if signedIn:
        return render_template('account.html')
    else:
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("log-in.html")

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        if email == '':
            return render_template("login-error.html", error='email is invalid')
        if password == '':
            return render_template("login-error.html", error='password is invalid')

        signedIn = True

        return render_template("account.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")

    if request.method == "POST":
        first = request.form.get('first')
        last = request.form.get('last')
        email = request.form.get('email')
        password = request.form.get('password')

        if first == '':
            return render_template("signup-error.html", error='first name is invalid')
        if last == '':
            return render_template("signup-error.html", error='last name is invalid')
        if email == '':
            return render_template("signup-error.html", error='email is invalid')
        if password == '':
            return render_template("signup-error.html", error='password is invalid')

        signedIn = True
        return render_template("account.html")


@app.route("/league/<name>")
def league(name=''):
    if (name == ''):
        return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
