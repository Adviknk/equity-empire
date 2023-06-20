from sqlalchemy import create_engine
import os


db_password = os.getenv("EQUITY_EMPIRE_DATABASE_PASSWORD")
db_string = "mysql+pymysql://9qnyibjw2viylcgcxr43:" + str(db_password) + \
    "@aws.connect.psdb.cloud/stock-trading-game?charset=utf8mb4"


engine = create_engine(
    db_string,
    connect_args={
        "ssl": {
            "ca": "/etc/ssl/cert.pem"
        }
    }
)
