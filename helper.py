from database import engine
from sqlalchemy import text


def load_users():
    with engine.connect() as conn:
        result = conn.execute(text("select * from users"))
        table = result.all()
        # lsit of dictionaries for each row
        result_dict = [row._asdict() for row in table]
        print(result_dict)
