import random
import ast


from database import engine
from sqlalchemy import text
from sqlHelper import *


def reset(league_id, cash):
    with engine.connect() as conn:
        array = get_ids(league_id=league_id)
        for user_id in array:
            string = "UPDATE " + str(league_id) + " SET amount=" + str(
                cash) + " WHERE user_id=" + str(user_id) + " AND stock='CASH'"
            conn.execute((text(string)))

        second_string = "UPDATE " + \
            str(league_id) + " SET valid = FALSE WHERE stock <> 'CASH';"
        conn.execute((text(second_string)))


def check_weeks(league_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        if (table[0][6] > get_week_check(league_id=league_id)):
            return True
    return False


def update_standing(league_id, matchups):
    users = get_ids(league_id=league_id)
    print(users)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM " + str(league_id)))
        leagues = result.all()
        result_dict = [row._asdict() for row in leagues]
        for matchup in matchups:
            for row in result_dict:
                if (row['user_id'] == users[matchup[0] - 1] and row['stock'] == 'CASH'):
                    cash1 = float(row['amount'])
                if (row['user_id'] == users[matchup[0] - 1] and row['stock'] == 'WINS'):
                    win1 = int(row['amount'])
                if (row['user_id'] == users[matchup[0] - 1] and row['stock'] == 'LOSSES'):
                    loss1 = int(row['amount'])
                if (row['user_id'] == users[matchup[1] - 1] and row['stock'] == 'CASH'):
                    cash2 = float(row['amount'])
                if (row['user_id'] == users[matchup[1] - 1] and row['stock'] == 'WINS'):
                    win2 = int(row['amount'])
                if (row['user_id'] == users[matchup[1] - 1] and row['stock'] == 'LOSSES'):
                    loss2 = int(row['amount'])

            if (cash1 > cash2):
                win1 = win1 + 1
                loss2 = loss2 + 1
                conn.execute(text("UPDATE " + str(league_id) + " SET amount=" + str(win1) +
                             " WHERE user_id=" + str(users[matchup[0] - 1]) + " AND stock='WINS'"))
                conn.execute(text("UPDATE " + str(league_id) + " SET amount=" + str(loss2) +
                             " WHERE user_id=" + str(users[matchup[1] - 1]) + " AND stock='LOSSES'"))

            else:
                loss1 = loss1 + 1
                win2 = win2 + 1
                conn.execute(text("UPDATE " + str(league_id) + " SET amount=" + str(win2) +
                             " WHERE user_id=" + str(users[matchup[1] - 1]) + " AND stock='WINS'"))
                conn.execute(text("UPDATE " + str(league_id) + " SET amount=" + str(loss1) +
                             " WHERE user_id=" + str(users[matchup[0] - 1]) + " AND stock='LOSSES'"))


def create_dict(league_id):
    players = []
    with engine.connect() as conn:
        leagues = conn.execute(
            text("SELECT * FROM " + str(league_id) + " WHERE stock = 'WINS'"))
        leagues_table = leagues.all()
        result_dict = [row._asdict() for row in leagues_table]
        for row in result_dict:
            players.append({"name": str(
                get_name(user_id=row['user_id'])), "wins": int(row['amount'])})

        i = 0
        leagues = conn.execute(
            text("SELECT * FROM " + str(league_id) + " WHERE stock = 'LOSSES'"))
        leagues_table = leagues.all()
        result_dict = [row._asdict() for row in leagues_table]
        for row in result_dict:
            players[i].update(
                {"losses": int(row['amount'])})
            total = players[i]["wins"] + \
                players[i]["losses"]
            if total == 0:
                total = 1
            players[i].update({"win_percentage": round(float(
                players[i]["wins"] / total), 3)})
            i = i + 1

    return players


def generate_schedule(num_teams, num_weeks):

    teams = list(range(1, num_teams + 1))
    schedule = []

    for week in range(1, num_weeks + 1):
        matchups = []
        random.shuffle(teams)

        for i in range(0, num_teams, 2):
            team1 = teams[i]
            team2 = teams[i + 1]
            matchups.append((team1, team2))

        schedule.append(matchups)

    return schedule


def add_schedule(league_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            array = generate_schedule(num_teams=int(
                row['num_players']), num_weeks=int(row['weeks']))
            conn.execute(text("UPDATE leagues SET schedule = '" +
                         str(array) + "' WHERE league_id = '" + str(league_id) + "'"))


def get_league_cash(league_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            return row['weekly_money']


def get_schedule(league_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            array_string = row['schedule']
            array = ast.literal_eval(array_string)
            return array

    return []


def get_ids(league_id):
    array = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            array_string = row['users']
            array = ast.literal_eval(array_string)

    return array


def get_names(league_id):
    names = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM leagues WHERE league_id = '" + str(league_id) + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            array_string = row['users']
            array = ast.literal_eval(array_string)

    for element in array:
        names.append(get_name(element))

    return names


def get_name(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (user_id == int(row['id'])):
                return row['username']


def get_week(league_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league_id) + " WHERE stock = 'WEEK'"))

        return int(result.all()[0][3])


def get_week_check(league_id):
    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM " + str(league_id) + " WHERE stock = 'WEEK-CHECK'"))

        return int(result.all()[0][3])


def add_week_check(league_id):
    with engine.connect() as conn:
        num = get_week_check(league_id) + 1
        conn.execute(text("UPDATE " + str(league_id) +
                     " SET amount=" + str(num) + " WHERE stock='WEEK-CHECK'"))


def add_week(league_id):
    with engine.connect() as conn:
        num = get_week(league_id) + 1
        conn.execute(text("UPDATE " + str(league_id) +
                     " SET amount=" + str(num) + " WHERE stock='WEEK'"))
