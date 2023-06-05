from sqlalchemy import create_engine

db_string = "mysql+pymysql://iqfzg8lbhpiy4qc7wtzu:pscale_pw_6IY8Vgm2eYoNVZROiqGPDu2iKr2pyG4Be0elSxL7v75@aws.connect.psdb.cloud/stock-trading-game?charset=utf8mb4"


engine = create_engine(
    db_string,
    connect_args={
        "ssl": {
            "ca": "/etc/ssl/cert.pem"
        }
    }
)
