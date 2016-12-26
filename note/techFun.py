import numpy as np
import scipy as sp
import pandas as pd

def updown(ret):
	'show the daily up or down'
	return np.sign(ret[:-1] - ret[1:])

def MA(ret, nvola):
    "moving average" 
    length_company = len(ret)
    vola_company = [-1] * length_company#default 
    if length_company < nvola:
    	return vola_company

    for j in range(length_company - nvola+1):
    	vola_j=ret[j:(j + nvola)]
    	vola_company[j] = sp.mean(vola_j)
    return vola_company

def VOL(ret,nvola):
	"historical volatility"
	length_company = len(ret)
	vola_company = [-1] * length_company
	if length_company < nvola:
		return vola_company

	for j in range(length_company-nvola+1):
		vola_j = ret[j:(j+nvola)]
		vola_company[j] = sp.sqrt(sp.var(vola_j))

	return vola_company

def RSI(closeprice,nRSIperiod):
	'require the closeprise to be pd.dataframe'
	length_company=len(closeprice.values)
	gainloss_company= closeprice.values[:-1] - closeprice.values[1:]
	RSI_company = [-1] * length_company
	if length_company<=nRSIperiod:
		return RSI_company

	for j in range(length_company-nRSIperiod+1):
		gainloss_j=gainloss_company[j:(j+nRSIperiod)]
		gain_j = gainloss_j[gainloss_j >= 0]
		loss_j = gainloss_j[gainloss_j <0 ]
		avegain_j = sum(gain_j)/nRSIperiod
		aveloss_j = sum(loss_j)/nRSIperiod
		RSI_company[j] = 100 - 100/(1+avegain_j/abs(aveloss_j))
	return RSI_company










