import yfinance as yf


from database import engine
from sqlalchemy import text


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


# def get_costs(league, user_id):
#     costs = []
#     with engine.connect() as conn:
#         result = conn.execute(
#             text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id)))
#         table = result.all()
#         result_dict = [row._asdict() for row in table]
#         for row in result_dict:
#             if (not (row['stock'] == 'CASH')):
#                 current_costs = float(row['cost'])
#                 costs.append(current_costs)

#     return costs


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


def cashout(league, user_id, stock):
    total = 0
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id) + " and stock = '" + stock + "'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            if (int(row['valid']) == 1):
                amount = int(row['amount'])
                total = total + amount

        if total == 0:
            return False

        result = conn.execute(
            text("SELECT * FROM " + str(league) + " WHERE user_id = " + str(user_id) + " and stock = 'CASH'"))
        table = result.all()
        result_dict = [row._asdict() for row in table]
        for row in result_dict:
            cash = round(float(row['amount']), 2)

        ticker = yf.Ticker(stock)
        stock_info = ticker.info
        current_price = stock_info["currentPrice"]

        cash = cash + current_price * total
        new_cash = round(cash, 2)

        update_string = "UPDATE " + str(league) + " SET amount = " + str(
            new_cash) + " WHERE user_id = " + str(user_id) + " and stock = 'CASH'"
        conn.execute(text(update_string))

        update_string = "UPDATE " + \
            str(league) + " SET valid = FALSE WHERE user_id = " + \
            str(user_id) + " and stock = '" + stock + "'"
        conn.execute(text(update_string))

        return True


def get_values(stocks, value):
    values = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_info = ticker.info
        current_price = stock_info[value]
        values.append(current_price)

    return values


def get_values_array(stock, values):
    return_values = []
    ticker = yf.Ticker(stock)
    stock_info = ticker.info
    for value in values:
        return_values.append(stock_info[value])

    return return_values
