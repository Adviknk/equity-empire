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
            "SELECT * FROM " + str(league) + " WHERE user_id = " + str(id) + " and stock = 'CASH'"))
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
            new_cash) + " WHERE user_id = " + str(id) + " and stock = 'CASH'"
        conn.execute(text(update_string))
        add_stock = "INSERT INTO " + \
            str(league) + " (user_id, stock, amount, valid, cost) VALUES (" + \
            str(id) + ", '" + str(stock) + "', " + str(num) + \
            ", TRUE, " + str(current_price) + ")"
        conn.execute(text(add_stock))
        return True


def get_costs(league, user_id):
    costs = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id)))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (not (row['stock'] == 'CASH')):
                current_costs = float(row['cost'])
                costs.append(current_costs)

    return costs


def get_costs(league, user_id):
    costs = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id)))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (not (row['stock'] == 'CASH') and int(row['valid']) == 1):
                current_costs = float(row['cost'])
                costs.append(current_costs)

    return costs


def get_stocks(league, user_id):
    stocks = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id)))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (not (row['stock'] == 'CASH') and int(row['valid']) == 1):
                current_stock = row['stock']
                stocks.append(current_stock)

    return stocks


def get_cash(league, user_id):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id) + " and stock = 'CASH'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            cash = float(row['amount'])

    return cash


def get_amounts(league, user_id):
    amount = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id)))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (not (row['stock'] == 'CASH') and int(row['valid']) == 1):
                current_amount = int(row['amount'])
                amount.append(current_amount)

    return amount
