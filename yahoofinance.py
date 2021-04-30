import yfinance as yf
from datetime import date, datetime


def get_stock_data(symbol, period, date_from):

    def parse_interval(period_code):
        if period_code == "1m":
            return "1d", "1m"
        elif period_code == "5m":
            return "1d", "5m"
        elif period_code == "15m":
            return "1d", "15m"
        elif period_code == "30m":
            return "1d", "30m"
        elif period_code == "1h":
            return "1d", "1h"
        elif period_code == "4h":
            return "1d", "1h"
        elif period_code == "1d":
            return "1d", "1d"
        elif period_code == "1w":
            return "1w", "1wk"
        else:
            return "", ""

    period, interval = parse_interval(period)
    dt_object = date_from.strftime("%Y-%m-%d")
    msft = yf.Ticker(symbol)
    hist = msft.history(start=dt_object,
                        period=period, interval=interval)
    return hist
