from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/add")
def add():
    return "testing extension"


@app.route("/signup")
def sign_in():
    return render_template('sign-up.html')


@app.route("/login")
def log_in():
    return render_template('log-in.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
