from database import engine
from sqlalchemy import text
import json


def load_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        # lsit of dictionaries for each row
        result_dict = [row._asdict() for row in table]


def authenticate(username, email, password):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (username == row['username'] and email == row['email'] and password == row['pwd']):
                return True

    return False


def exists(username):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (username == row['username']):
                return True

    return False


def get_id(username):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (username == row['username']):
                return row['id']

    return 0


def get_league_id(name):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM leagues"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (name == row['name']):
                return row['league_id']

    return 0


def league_exists(name):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM leagues"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (name == row['name']):
                return True

    return False


def add_user(first, last, username, email, password):
    with engine.connect() as conn:
        result = conn.execute(text("INSERT INTO users (firstName, lastName, username, email, pwd, leagues) VALUES ('" +
                              first + "', '" + last + "', '" + username + "','" + email + "','" + password + "','[]')"))


def get_leagues(username):
    leagues = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (username == row['username']):
                leagues = json.loads(row['leagues'])

    names = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM leagues"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            for league in leagues:
                if (league == row['id']):
                    names.append(row['name'])
    return names


def create_league(id, name, password, players, start, weeks, cash, username):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO leagues (name, league_id, password, num_players, start_date, weeks, weekly_money, users) VALUES ('" +
                          name + "', '" + id + "', '" + password + "'," + str(players) + ",'" + start + "', " + str(weeks) + ", " + str(cash) + ", '" + '[' + str(username) + ']' + "')"))
        leagues = conn.execute(text("SELECT * FROM leagues"))
        users = conn.execute(text("SELECT * FROM users"))
        leagues_table = leagues.all()
        users_table = users.all()
        result_dict = [row._asdict() for row in leagues_table]
        for row in result_dict:
            if (id == row['league_id']):
                league_id = row['id']

        leagues = []
        result_dict = [row._asdict() for row in users_table]
        for row in result_dict:
            if (username == row['id']):
                leagues = json.loads(row['leagues'])

        leagues.append(league_id)
        conn.execute(text("UPDATE users SET leagues = '" +
                     str(leagues) + "' WHERE id = " + str(username)))

        create_leagure_string = "CREATE TABLE " + id + \
            " (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, user_id INT, stock VARCHAR(100), amount INT, valid BOOLEAN)"
        conn.execute(text(create_leagure_string))
        add_first_user = "INSERT INTO " + id + \
            "(user_id, stock, amount, valid) VALUES (" + \
            str(username) + ",'CASH', " + str(cash) + ", TRUE)"
        conn.execute(text(add_first_user))


def correct(id, name, password):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM leagues"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (id == row['league_id'] and name == row['name'] and password == row['password']):
                return True

    return False


def join_league(id, name, password, user_id):
    with engine.connect() as conn:
        leagues = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + id + "'"))
        users = conn.execute(
            text("SELECT * FROM users WHERE id = " + str(user_id)))
        leagues_table = leagues.all()
        users_table = users.all()
        result_dict = [row._asdict() for row in leagues_table]
        league_id = 0
        cash = 0
        users_array = []
        for row in result_dict:
            if (id == row['league_id']):
                league_id = row['id']
                cash = row['weekly_money']
                users_array = json.loads(row['users'])
        users_array.append(user_id)
        conn.execute(text("UPDATE leagues SET users = '" +
                     str(users_array) + "' WHERE id = " + str(league_id)))

        leagues = []
        result_dict = [row._asdict() for row in users_table]
        for row in result_dict:
            if (user_id == row['id']):
                leagues = json.loads(row['leagues'])

        leagues.append(league_id)
        conn.execute(text("UPDATE users SET leagues = '" +
                     str(leagues) + "' WHERE id = " + str(user_id)))

        add_curr_user = "INSERT INTO " + id + \
            "(user_id, stock, amount, valid) VALUES (" + \
            str(user_id) + ",'CASH', " + str(cash) + ", TRUE)"
        conn.execute(text(add_curr_user))
