#!usr/bin/env python

'''
construct a stockSeries class to faciliate the technical analysis on stock data from tushare package
'''
import numpy as np
import pandas as pd
import datetime
import tushare as tu
import matplotlib.pyplot as plt
import ohlcvPlot

import plotly.plotly as py
import cufflinks as cf
import plotly.graph_objs as go
from plotly import tools
cf.set_config_file(world_readable=True,offline=False)

class stockSeries(pd.core.frame.DataFrame):
    def sma(self, window):
        if len(self) < window:
            return None
        result=map(lambda x:sum(self['close'].iloc[-x:(-x+window)]) / float(window)
                   , [i for i in range(len(self)+1) if i>window])
        return pd.Series(result[::-1],index=self.index[:-window])
    def ema_genereator(self, window):
        c = 2.0 / float(window + 1)
        ema_t=sum(self['close'].iloc[-window:]) / float(window)
        t=window+1
        while True:
            yield ema_t
            ema_t= c*self['close'].iloc[-t]+(1-c)*ema_t
            t=t+1
    def ema(self,window):
        g=self.ema_genereator(window)
        result= [g.next() for i in range(len(self)-window+1)]
        return pd.Series(result[::-1],index=self.index[:-window+1])
    def macd(self,fasterwindow=12,slowerwindow=26,signalwindow=9):
        result= pd.DataFrame({fasterwindow:self.ema(fasterwindow),
                              slowerwindow:self.ema(slowerwindow)}).sort_index(axis=0 ,ascending=False)
        result['macd']=result[fasterwindow]-result[slowerwindow]
        temp=stockSeries({'close':result['macd']})
        temp=temp.dropna()
        temp=stockSeries({'close':temp['close']})
        result[signalwindow]=temp.ema(signalwindow)
        
        result['Signal'] = result['macd']-result[signalwindow]
        return result
    
    def plot_macd(self,fasterwindow=12,slowerwindow=26,signalwindow=9,ohlcinclude=False,stock_name=''):
        self.columns = [x.lower() for x in self.columns]#bug using ohlcvPlot beforehand
        result=self.macd(fasterwindow,slowerwindow,signalwindow)
        if ohlcinclude:
            fig = tools.make_subplots(rows=2, cols=1,shared_xaxes=True, shared_yaxes=True)
            trace1 = go.Candlestick(x=self.index,
                                   open=self.open,
                                   high=self.high,
                                   low=self.low,
                                   close=self.close)
            trace2= go.Scatter(x=result.index,
                              y=result.macd,name='macd')
            trace3= go.Scatter(x=result.index,
                              y=result[signalwindow],name='9EMA')
            trace4=go.Bar(x=result.index,
                         y=result.macd-result[signalwindow],name='macd-9ema')
            fig.append_trace(trace1, 1, 1)
            fig.append_trace(trace2, 2, 1)
            fig.append_trace(trace3, 2, 1)
            fig.append_trace(trace4, 2, 1)            
            fig['layout'].update(height=800, width=1000, title=stock_name)
            try:
                py.iplot(fig)
            except:
                print "hit the limit of plotly try matplotlib"
                ohlcvPlot.pandas_candlestick_ohlcv(self)

        else:
            try:
                result[['macd',signalwindow]].iplot(kind='scatter')
            except:
                print "hit the limit of plotly try matplotlib"
                result[['macd',signalwindow]].iloc[::-1].plot()

            
   