import pandas as pd
import numpy as np
from datetime import date


def getSupport(df, i):
    supportPrice = 0
    if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]:
        supportPrice = df['Low'][i]

    return supportPrice


def getResistance(df, i):
    resistancePrice = 0
    if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]:
        resistancePrice = df['High'][i]

    return resistancePrice


def get_support_resistance_lines(df):
    allPrices = []
    for i in range(2, df.shape[0] - 2):
        supportPrice = getSupport(df, i)
        resistantPrice = getResistance(df, i)
        if supportPrice != 0:
            allPrices.append((i, supportPrice))
        elif resistantPrice != 0:
            allPrices.append((i, resistantPrice))

    # df['Date'] = pd.to_datetime(df.index)
    # df['Date'] = df['Date'].apply(mpl_dates.date2num)
    # df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    # get rid of prices near to one another reduce noise

    mean = np.mean(df['High'] - df['Low'])  # rough estimate of volatility

    allPrices = []

    for i in range(2, df.shape[0] - 2):
        supportPrice = getSupport(df, i)
        resistantPrice = getResistance(df, i)
        if supportPrice != 0:
            if np.sum([abs(supportPrice-x) < mean for x in allPrices]) == 0:
                allPrices.append((i, supportPrice))
        elif resistantPrice != 0:
            if np.sum([abs(resistantPrice-x) < mean for x in allPrices]) == 0:
                allPrices.append((i, resistantPrice))

    sr_lines = []
    for item in allPrices:
        sr_lines.append((df.iloc[item[0]].name, item[1]))
    return sr_lines


def get_overnight_gapper(df, minPrice=0.20, percentGapper=0.05):
    on_gappers = []
    for i in range(0, df.shape[0]-2):
        overnightGapper = 0
        gap = df['Close'][i] - df['Open'][i+1]
        calcPercent = abs(gap / df['Close'][i])
        if calcPercent >= percentGapper and abs(gap) >= minPrice:
            on_gappers.append((i, df['Close'][i]))
            on_gappers.append((i, df['Open'][i+1]))

    return on_gappers
