import random
import ast
from database import engine
from sqlalchemy import text
from sqlHelper import *


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
