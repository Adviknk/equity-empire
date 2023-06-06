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


def league_exists(name):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM leagues"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (name == row['league_id']):
                return True

    return False


def add_user(first, last, username, email, password):
    with engine.connect() as conn:
        result = conn.execute(text("INSERT INTO users (firstName, lastName, username, email, pwd) VALUES ('" +
                              first + "', '" + last + "', '" + username + "','" + email + "','" + password + "')"))


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


def join_league():
    return 0
