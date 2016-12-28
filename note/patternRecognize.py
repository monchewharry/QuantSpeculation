import talib

def patterns(ohcl):

  patternFun=talib.get_function_groups()['Pattern Recognition']#can customize
  input = [ohcl['open'].values,ohcl['high'].values,ohcl['low'].values,ohcl['close'].values]
  for f in patternFun:
    ohcl[f]=eval("talib.%s(*input)"%f)#add columns