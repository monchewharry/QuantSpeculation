import numpy as np
from peakutils.peak import indexes

def peakDetect(ret,thred=0.5,min_dist=5):
	loc = indexes(ret, thres=thred, min_dist=min_dist)
	print('Peaks are: %s' % (loc))
	return loc