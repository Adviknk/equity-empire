import yfinance as yf
from database import engine
from sqlalchemy import text
import json


# Define a list of top stock symbols
# top_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "JPM", "V", "JNJ", "NVDA",
#                "PYPL", "UNH", "HD", "PG", "MA", "DIS", "BAC", "INTC", "XOM", "VZ"]


def processOrder(stock, num):
    try:
        ticker = yf.Ticker(stock)
        stock_info = ticker.info
        current_price = stock_info["currentPrice"]
        print(current_price)
        return True
    except Exception:
        return False


def buyStock(stock, num, league, id):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM " + str(league) + " WHERE id = " + str(id) + " and stock = 'CASH'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            cash = float(row['amount'])

        ticker = yf.Ticker(stock)
        stock_info = ticker.info
        current_price = stock_info["currentPrice"]
        cost = float(current_price) * float(num)
        if (cash < cost):
            return False

        new_cash = cash - cost

        update_string = "UPDATE " + str(league) + " SET amount = " + str(
            new_cash) + " WHERE id = " + str(id) + " and stock = 'CASH'"
        conn.execute(text(update_string))
        add_stock = "INSERT INTO " + \
            str(league) + " (user_id, stock, amount, valid) VALUES (" + \
            str(id) + ", '" + str(stock) + "', " + str(num) + ", TRUE)"
        conn.execute(text(add_stock))
        return True
