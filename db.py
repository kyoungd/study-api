#!/usr/bin/python
import psycopg2
from config import config
from datetime import datetime, timedelta, date
from yahoofinance import get_stock_data
from study import get_support_resistance_lines
import pandas as pd
import json


def read_study_from_db(conn, study_type, symbol, period, current_date):
    try:
        one_date = datetime(
            current_date.year, current_date.month, current_date.day)
        """ read from support_resistance table """
        cur = conn.cursor()

        sql = """SELECT data FROM studies where study_type=%s and symbol=%s and period=%s and published_on >= %s"""
        # execute the SELECT statement
        cur.execute(sql, (study_type, symbol, period, one_date,))
        # get the generated id back
        result = cur.fetchone()
        if (result == None):
            return None
        data = json.dumps(result[0])
        conn.commit()
        if (study_type == "DT"):
            return True, pd.read_json(data, orient="split")
        else:
            return True, data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False, None


def save_study_to_db(conn, study_type, symbol, period, current_date, df_data):
    one_date = datetime(
        current_date.year, current_date.month, current_date.day)
    """ insert a new vendor into the vendors table """
    cur = conn.cursor()

    sql = """INSERT INTO studies (study_type, symbol, period, published_on, data)
             VALUES(%s, %s, %s, %s, %s) RETURNING id;"""
    id = None
    # execute the INSERT statement
    if (study_type == "DT"):
        data = df_data.to_json(orient="split")
        cur.execute(sql, (study_type, symbol,
                          period, current_date, data,))
    else:
        data = json.dump(df_data)
        cur.execute(sql, (study_type, symbol,
                          period, current_date, data,))
    # get the generated id back
    id = cur.fetchone()[0]
    conn.commit()
    return id


def get_start_date(period, current_date):
    one_date = datetime(
        current_date.year, current_date.month, current_date.day)
    if (period == "1m"):
        return one_date + timedelta(days=-5)
    elif (period == "5m"):
        return one_date + timedelta(days=-5)
    elif (period == "15m"):
        return one_date + timedelta(days=-10)
    elif (period == "30m"):
        return one_date + timedelta(days=-30)
    elif (period == "1h"):
        return one_date + timedelta(days=-90)
    elif (period == '4h'):
        return one_date + timedelta(days=-180)
    elif (period == "1d"):
        return one_date + timedelta(days=-366)
    elif (period == "1w"):
        return one_date + timedelta(days=-1096)
    else:
        return None


def db_connection():
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    return conn


def process_study(symbol, period, func):
    """ Connect to the PostgreSQL database server """
    conn = None
    sr_lines = []
    try:
        conn = db_connection()
        isQuoteValid = False
        isQuoteValid, quotes = read_study_from_db(
            conn, "DT", symbol, period, datetime.today())
        if not isQuoteValid:
            current_time = datetime.today()
            date_from = get_start_date(period, current_time)
            quotes = get_stock_data(symbol, period, date_from)
            save_study_to_db(conn, "DT", symbol, period,
                             current_time, quotes)
            print('db update complete')
        sr_lines = func(quotes)
        print('return support/resistance data')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return sr_lines


def get_study(study_type, symbol, period):
    if study_type == "SR":
        return process_study(symbol, period, get_support_resistance_lines)
    elif study_type == "OG":
        return process_study(symbol, "1d", get_overnight_gapper)
    else:
        return []


if __name__ == '__main__':
    get_study('SR', 'SYPR', "1d")


# def get_date_from(conn, cur, symbol, period):
#     sql = """SELECT MAX(quote_date) FROM stocks WHERE symbol=%s AND period=%s"""
#     one_date = None
#     try:
#         cur.execute(sql, (symbol, period,))
#         result = cur.fetchone()
#         one_date = result[0]
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     return one_date


# def read_quotes_from_db(symbol, period, date_from):
#     one_date = datetime.datetime(
#         current_date.year, current_date.month, current_date.day)
#     """ read from support_resistance table """
#     cur = conn.cursor()

#     sql = """SELECT * FROM stocks where symbol=%s and period=%s and quote_date >= %s"""
#     # execute the SELECT statement
#     cur.execute(sql, (study_type, symbol, period, one_date,)))
#         # get the generated id back
#         result=cur.fetchall()
#         conn.commit()
#         return result


# def insert_one_quote(conn, symbol, period, quote_date, openq, close, high, low, volume, dividend, stock_split):
#     """ insert a new vendor into the vendors table """
#     cur = conn.cursor()

#     sql = """INSERT INTO stocks (symbol, period, quote_date, open, close, high, low, volume, dividend, stock_split)
#              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
#     id = None
#     # execute the INSERT statement
#     cur.execute(sql, (symbol, period, quote_date, openq,
#                 close, high, low, volume, dividend, stock_split,))
#     # get the generated id back
#     id = cur.fetchone()[0]
#     conn.commit()
#     return id
