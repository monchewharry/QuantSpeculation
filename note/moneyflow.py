'''
 "accumulating," or buying, 
 "distributing," or selling, 
 http://www.investopedia.com/articles/trading/08/accumulation-distribution-line.asp
'''
import pandas as pd
import numpy as np
import datetime

def adline(ohclv,stick):
	ohclv.columns = [x.title() for x in ohclv.columns]
	ohclv.index = [pd.to_datetime(date) for date in ohclv.index]
	if ohclv.index[0] > ohclv.index[1]:#tushare need reversing
		ohclv = ohclv.reindex(index=ohclv.index[::-1])

	transdat = ohclv.loc[:,["Open", "High", "Low", "Close","Volume"]]
	# Create a new DataFrame newdat which includes OHLCV data for each period specified by period input
	if (type(stick) == str):
	    if stick == "day":
	        newdat = transdat
	        stick = 1 

	    elif stick in ["week", "month", "year"]:
	        if stick == "week":
	            transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
	        elif stick == "month":
	            transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months

	        transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
	        grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable

	        newdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": [],"Volume":[]}) # Create empty data frame containing what will be plotted
	        for name, group in grouped:
	            newdat = newdat.append(pd.DataFrame({"Open": group.iloc[0,0],
	                                        "High": max(group.High),
	                                        "Low": min(group.Low),
	                                        "Close": group.iloc[-1,3],
	                                        "Volume": sum(group.Volume)},
	                                       index = [group.index[0]]))
	        if stick == "week": stick = 5
	        elif stick == "month": stick = 30
	        elif stick == "year": stick = 365
	
	elif (type(stick) == int and stick >= 1):
	    transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
	    grouped = transdat.groupby("stick")
	    newdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": [],'Volume':[]}) # Create empty data frame containing what will be plotted

	    for name, group in grouped:
	        newdat = newdat.append(pd.DataFrame({"Open": group.iloc[0,0],
	                                    "High": max(group.High),
	                                    "Low": min(group.Low),
	                                    "Close": group.iloc[-1,3],
	                                    'Volume':sum(group.Volume)},
	                                   index = [group.index[0]]))
	
	else:
	    raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')
	newdat.loc[:,'Clv'] = (newdat['Close'] - newdat['Low'] - 
               newdat['High'] + newdat['Close'])/(newdat['High']-newdat['Low'])
	newdat.loc[:,'Adline'] = newdat['Clv'] * newdat['Volume']
	return newdat

