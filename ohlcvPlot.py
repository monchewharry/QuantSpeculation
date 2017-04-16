import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt 
from matplotlib.dates import date2num, DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc

#https://pythonprogramming.net/advanced-matplotlib-graphing-charting-tutorial/

def pandas_candlestick_ohlcv(dat, stick = "day", otherseries = None, adline= None):
    dat.columns = [x.title() for x in dat.columns]#compatible from tushare
    dat.index=[pd.to_datetime(date) for date in dat.index]
    if dat.index[0] > dat.index[1]:
        dat = dat.reindex(index=dat.index[::-1])

    transdat = dat.loc[:,["Open", "High", "Low", "Close","Volume"]]
    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
            grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": [],"Volume":[]}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3],
                                            "Volume":sum(group.Volume)},
                                           index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365
 
    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": [],"Volume":[]}) # Create empty data frame containing what will be plotted

        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3],
                                        "Volume":sum(group.Volume)},
                                       index = [group.index[0]]))
 
    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    # Set plot parameters, including the axis object ax used for plotting
    mondays = WeekdayLocator(MONDAY)    # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    dayFormatter = DateFormatter('%d')      # e.g., 12
    
    fig = plt.figure(facecolor='#07000d',figsize=(15, 8))
    ax = plt.subplot2grid((8,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')

    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')

    #############OHCL part###############    
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.grid(True)
    ax.yaxis.label.set_color("w")
    ax.spines['bottom'].set_color("#5998ff")
    ax.spines['top'].set_color("#5998ff")
    ax.spines['left'].set_color("#5998ff")
    ax.spines['right'].set_color("#5998ff")
    ax.tick_params(axis='y', colors='w')
    ax.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    # Create the candelstick chart
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())),
                        plotdat["Open"].tolist(), plotdat["High"].tolist(),
                        plotdat["Low"].tolist(), plotdat["Close"].tolist()) ),
                     colordown='#53c156', colorup='#ff1717', width = stick * .4)
 
    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
 
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')#rotate the label

    #############volume part###############
    volumeMin = 0
    volume = plotdat['Volume']
    ax1v = ax.twinx()
    ax1v.fill_between(plotdat.index,volumeMin, volume, facecolor='#00ffe8', alpha=.4)
    ax1v.axes.yaxis.set_ticklabels([])
    ax1v.grid(False)
    ###Edit this to 3, so it's a bit larger
    ax1v.set_ylim(0, 3*volume.max())
    ax1v.spines['bottom'].set_color("#5998ff")
    ax1v.spines['top'].set_color("#5998ff")
    ax1v.spines['left'].set_color("#5998ff")
    ax1v.spines['right'].set_color("#5998ff")
    ax1v.tick_params(axis='x', colors='w')
    ax1v.tick_params(axis='y', colors='w')

    #############ADLine part###############
    if adline != None:
        adlineMin  = min(dat[adline])
        ax2 = plt.subplot2grid((8,4), (6,0), sharex=ax, rowspan=2, colspan=4)
        width = stick * .4
        ax2.xaxis.set_major_formatter(weekFormatter)

        ax2.bar(plotdat.index, dat[adline],width,color="#53c156")

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel('ADLine', color='w')
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')#
    plt.show()