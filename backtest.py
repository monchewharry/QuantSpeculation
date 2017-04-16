#!usr/bin/env/ python

'''
construct a backtest class to faciliate the backtesting algorithm based on generated signal 
'''
import numpy as np
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc

class backtest():
    '''
    The time in the data_out input must be descending:from recent days to prior days
    Signal column is requuired in data_out input
    '''
    def __init__(self,data_out,price):
        self.data_out=data_out.dropna().iloc[::-1]#late to the last
        self.price=price.head(len(self.data_out)).iloc[::-1]
    def backtest(self,trade_size=100,ifshort=True):
        prev_x_amount = 0 #amount
        position = 0 #-1,0,1
        trade_size = trade_size
        signal = np.sign(self.data_out.Signal)#############
        self.data_out['buyOrsell']=signal
        x_amount = pd.Series(np.zeros(len(signal)),index=self.data_out.index)   
        if ifshort:
            for i in range(len(signal)) :
              if signal[i] == 1 and position == 0 :
                # buy the spread initially
                prev_x_amount = trade_size
                x_amount[i] = prev_x_amount
                position = 1

              if signal[i] == -1 and position == 0 :
                # sell the spread initially
                prev_x_amount =  trade_size
                x_amount[i] = -prev_x_amount
                position = -1

              if signal[i] == 1 and position == -1 :
                # we were short the spread and need to buy
                x_amount[i] = trade_size + prev_x_amount
                prev_x_amount = trade_size
                position = 1


              if signal[i] == -1 and position == 1 :
                # we are long the spread and need to sell
                x_amount[i] = -(trade_size + prev_x_amount)
                prev_x_amount = trade_size
                position = -1            
        else:
            for i in range(len(signal)) :
              if signal[i] == 1 and position == 0 :
                # buy the spread initially
                x_amount[i] = trade_size
                position = 1


              if signal[i] == -1 and position == 0 :
                # sell the spread initially
                x_amount[i] = 0
                position = 0

              if signal[i] == -1 and position == 1 :
                # we are long the spread and need to sell
                x_amount[i] = - trade_size 
                position = 0
            
        x_amount[len(x_amount)-1] = -sum(x_amount)#zero out
        self.data_out["x_amount"] = x_amount
        
        cash_buy=[(np.sign(q)==1)*q*self.price[i] for i,q in enumerate(self.data_out.x_amount) ]
        cash_sell=[-((np.sign(q)==-1)*q*self.price[i]) for i,q in enumerate(self.data_out.x_amount) ]
        pos = np.cumsum(self.data_out.x_amount)
        cumulative_buy = np.cumsum(cash_buy)#money outflow
        cumulative_sell = np.cumsum(cash_sell)#money inflow
        equity = (cumulative_sell - cumulative_buy) + pos * self.price#realized P&L+unrealized P&L
        self.data_out['equity_curve']=equity
        return self.data_out
        
    def plot_curve(self):
        data = [go.Scatter(
                  x=self.data_out.equity_curve.index,
                  y=self.data_out.equity_curve.values)]
        try:
            py.iplot(data)
        except:
            print "hit the limit of plotly, try matplotlib"
            self.data_out.equity_curve.plot()




