import time
from threading import Timer
import tushare as tu
#https://docs.python.org/2/library/sched.html#

#t=1
def monitorPrice(id,upexceed,dropexceed):
#	global t
#	print t
#	t += 1
	a = float(tu.get_realtime_quotes(id)['price'].values[0])
	if a <= dropexceed:
		print a
		print '\a'#sound
	elif a >= upexceed:
		print a
		print '\a'
	else:
		print 'normal'
	sched=Timer(30, monitorPrice, (id,upexceed,dropexceed))
	sched.start()
#	if t > 3:#stop condition
#		sched.cancel()

Timer(1, monitorPrice, ('150201',0.54,0.51)).start()

