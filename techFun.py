import numpy as np
import scipy as sp
import pandas as pd

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
