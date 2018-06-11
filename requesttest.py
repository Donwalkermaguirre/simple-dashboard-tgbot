# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#web= "http://127.0.0.1:5000/test_reception"
#web2="http://127.0.0.1:5000/testlogin"
#payload={'username':"jaime",'password':'casanova','typeplot':'series','date':'12','data':'NEWDATAAA2 bsbe'}
#payload={'username':"jaime",'password':'casanova'}
#s = requests.Session()
#r = s.post(web,data=payload)
#cont=r.content

web= "http://127.0.0.1:5000/senddata"

def delta_time_minutes(time):
	try:
		guess=datetime.strptime(time,'%H:%M')
		real_string="{}:{}".format(datetime.now().hour,datetime.now().minute)
		real=datetime.strptime(real_string,'%H:%M')
		if real>guess:
			delta=real-guess
		else:
			delta=guess-real
		return delta.seconds/60
	except:
		print "wrong format"
		return "wrong_format"

'''
payload={'username':"jaime",'password':'casanova','typeplot':'frequency','date':'12','data':'{}'.format(delta_time_minutes('13:55'))}	
r=requests.post(web,data=payload)
print r.content
'''
