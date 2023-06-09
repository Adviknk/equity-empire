import random
import ast
from database import engine
from sqlalchemy import text
from sqlHelper import *
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(daemon=True)
scheduler.start()


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


def get_week():
    return 1


def change_week():
    print(10)


def schedule_task():
    scheduler.add_job(change_week, 'date',
                      seconds=10)  # Set the desired time

    # Start the scheduler (if not already started)
    if not scheduler.running:
        scheduler.start()

    print("Task 2 scheduled successfully!")
