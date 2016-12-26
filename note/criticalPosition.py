from peakDetect import peakDetect 
import numpy as np
import pandas as pd

def criticalPos(vector ,nearest, period, thred,min_dist):
	loc = peakDetect(vector.values, thred, min_dist)#peaks
	loc2 = peakDetect(-vector.values, thred, min_dist)#bottoms
	l = [0] * len(vector)
	for i in loc:
		l[i]=i
	for i in loc2:
		l[i]=-i
	vect = pd.DataFrame({'close':vector,'loc+-':l})
	a=vect.iloc[loc[loc<=period]]

	if nearest:
		return a
	else:
		return a.sort('close',ascending=False)




