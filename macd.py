#!usr/bin/env python
'''
generate macd Signals
'''
import numpy as np
import pandas as pd
import datetime
import tushare as tu
from stockSeries import *
from backtest import *

def macd(stock,period):
	todaydate=datetime.datetime.now()
	start=todaydate-datetime.timedelta(days=period)
	stock_name=stock
	base_stock = tu.get_hist_data(stock_name,start=start.strftime('%Y-%m-%d'))
	macd_stock=stockSeries({'close':base_stock['close'],'open':base_stock['open'],
	               'high':base_stock['high'],'low':base_stock['low']})
	macd_out=macd_stock.macd(12,26,9)
	mb=backtest(macd_out,macd_stock.close)
	mb.backtest(trade_size=100,ifshort=True)
	mb.plot_curve()
	return mb.data_out

        
        
