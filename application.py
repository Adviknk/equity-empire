from flask import Flask, render_template, request, redirect, session
from helper import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_leagues = []


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
        # currently using leagues array but will use SQL array connected to the username
        return render_template('league-home.html', username=session['username'], all_leagues=user_leagues)
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
    if 'username' in session:
        return redirect('/account')

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
    if 'username' in session:
        return redirect('/account')

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


@app.route("/create/<username>", methods=["GET", "POST"])
def create(username=''):
    if 'username' in session:

        if request.method == "GET":
            return render_template('create.html', username=session['username'])

        if request.method == "POST":
            name = request.form.get('name')
            if name == '':
                return redirect('/leagues')

            # adding the league to the leagues
            # replace with SQL data
            user_leagues.append(name)

            return redirect('/leagues')

    else:
        return redirect('/login')


@app.route("/join/<username>", methods=["GET", "POST"])
def join(username=''):
    if 'username' in session:
        if request.method == "GET":
            return render_template('join.html', username=session['username'])

        if request.method == "POST":
            id = request.form.get('id')
            pwd = request.form.get('pwd')
            if id == '':
                return redirect('/leagues')

            # check if the id and pwd are correct and add that league to the
            # users leagues in SQL
            # each league will have an id and all information

            return redirect('/leagues')

    else:
        return redirect('/login')


@app.route("/leagues/<username>/<league_name>/portfolio")
def portfolio(username='', league_name=''):
    # also check if the username in session has a league with that name by checking database
    if 'username' in session:
        # check if league in username database
        if league_name in user_leagues:
            return render_template('portfolio.html', username=session['username'], name=league_name)

    return redirect('/login')


@app.route("/leagues/<username>/<league_name>/stocks")
def stocks(username='', league_name=''):
    # also check if the username in session has a league with that name by checking database
    if 'username' in session:
        # check if league in username database
        if league_name in user_leagues:
            return render_template('stocks.html', username=session['username'], name=league_name)

    return redirect('/login')


@app.route("/leagues/<username>/<league_name>/scoreboard")
def scoreboard(username='', league_name=''):
    # also check if the username in session has a league with that name by checking database
    if 'username' in session:
        # check if league in username database
        if league_name in user_leagues:
            return render_template('scoreboard.html', username=session['username'], name=league_name)

    return redirect('/login')


@app.route("/leagues/<username>/<league_name>/standings")
def standings(username='', league_name=''):
    # also check if the username in session has a league with that name by checking database
    if 'username' in session:
        # check if league in username database
        if league_name in user_leagues:
            return render_template('standings.html', username=session['username'], name=league_name)

    return redirect('/login')


@app.route("/leagues/<username>/<league_name>/schedule")
def schedule(username='', league_name=''):
    # also check if the username in session has a league with that name by checking database
    if 'username' in session:
        # check if league in username database
        if league_name in user_leagues:
            return render_template('schedule.html', username=session['username'], name=league_name)

    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
