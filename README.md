# QuantSpeculation

1. stockSeries class: `stockSeries.py`
2. backtest class: `backtest.py`
3. ohlc matplotlib function: `ohlcvPlot.py`

### example

```
todaydate=datetime.datetime.now()
start=todaydate-datetime.timedelta(days=200)
stock_name='601668'
base_stock =tu.get_hist_data(stock_name,start=start.strftime('%Y-%m-%d'))
a=stockSeries({'close':base_stock['close'],
'open':base_stock['open'],
'high':base_stock['high'],
'low':base_stock['low']})         
```

```
a.macd(12,26,9)
a.plot_macd(12,26,9,ohlcinclude=False,stock_name)
```  

```
m=backtest(data_out=a.macd(12,26,9),price=a.close)
m.backtest(trade_size=100,ifshort=True)
m.plot_curve()
```