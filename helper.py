from database import engine
from sqlalchemy import text
import json


def load_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        # lsit of dictionaries for each row
        result_dict = [row._asdict() for row in table]
        print(result_dict)


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
