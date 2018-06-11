#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from Utils2 import *
import time
import json 
import requests
import logging
import time
from datetime import datetime
TOKEN = '553928486:AAEuz0259OIqMy1ZDpc0YV6gWPAIZV-afvk'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = sqlite3.connect('mydb')
db2=sqlite3.connect('mydb_nonhashed')
logging.basicConfig(format='\n %(asctime)s - %(name)s - %(levelname)s - %(message)s\n',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js



def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
   
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            logging.debug("update id:{}".format(check_update_id(update)))
            word="test word"
            #word=webtest()
            chat = update["message"]["chat"]["id"]
            logging.debug("chat id:{}".format(chat))
            send_message(word, chat)
        except Exception as e:
            print(e)   

def check_update_id(update):
	u_id=update['message']['from']['id']   
	#a['result'][0]['message']['from']['id']
	return u_id

context={}  


	
	
def conversation(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            logging.debug("update id:{} and text{}".format(check_update_id(update),text))
            chat = update["message"]["chat"]["id"]
            exist=check_id_exist(chat,db)
            logging.debug("id exists:{}".format(exist))
            #provisional echo if exists here would go conversation
            ###
            if exist:
				conversation_plot(context,chat,db,text)
###LOGIN/REgistration script###
            else:							
				if not context.has_key(chat):
					context[chat]={}
					context[chat]['state']=None
				choosing(context,chat,db,text)
				###LOGIN/REgistration script###            
				logging.debug("chat id:{}".format(chat))
				#Conditionals inside functions
				if context[chat]['state']:
					register(context,chat,db,text,db2)
					login(context,chat,db,text)
				logging.debug(" post conversation context:{}".format(context))
				###LOGIN/REgistration script end###
        except Exception as e:
            print(e)  


def notkey(chat,context):
	if not context.has_key(chat):
		context[chat]={}
		context[chat]['state']=None
	return context
	



		
def check_valid_arg(message):
	v1=('register'==message)
	v2=('login'==message)
	return v1 or v2
		
	
	
	
	
	
	  
  
def choosing(context,ids,db,message):
	logging.debug('INSIDE CHOOSING CONTEXT:{} MESSAGE {}'.format(context,message))
	if not context[ids]['state']:
		context[ids]['state']='choosing'
		logging.debug('modifying state to choosing')
		send_message("Choose login or register",ids)
	elif context[ids]['state']=='choosing':
		if check_valid_arg(message):
			context[ids]['state']=message
			logging.debug('modifying state to {}'.format(message))
		else:
			send_message('unknown command',ids)





  
   
def register(context,ids,db,message,db2):
	if context[ids]['state']=='register':
		context[ids]['state']='user_r'
		logging.debug('modifying state to user_r')
		#change this for sendmessage
		send_message("enter your username", ids)
	elif context[ids]['state']=='user_r':
		context[ids]['data']={}
		if check_user_exists(message,db):
			logging.debug(" user exist")
			send_message("taken,try another username pal", ids)
			return
		
		context[ids]['data']['username']=message	
		context[ids]['state']='user_p'
		logging.debug('setting username and state to user_p')
		#change for sendmessage
		send_message("enter your password", ids)
	elif context[ids]['state']=='user_p':
		context[ids]['data']['password']=message
		context[ids]['state']=None
		logging.debug('setting password and reseting state ')
		insert_db_users(ids,context[ids]['data']['username'],context[ids]['data']['password'],db)
		insert_db_users_nonhashed(ids,context[ids]['data']['username'],context[ids]['data']['password'],db2)
		del context[ids]
		logging.debug('entrying database and deleting data in context ')
		send_message("DONE", ids)









def login(context,ids,db,message):
	if context[ids]['state']=='login':
		context[ids]['state']='user_l'
		logging.debug('modifying state to user_r')
		#change this for sendmessage
		send_message("enter your username", ids)
	elif context[ids]['state']=='user_l':
		context[ids]['data']={}
		context[ids]['data']['username']=message	
		context[ids]['state']='user_lp'
		logging.debug('setting username and state to user_lp')
		#change for sendmessage
		send_message("enter your password", ids)
	elif context[ids]['state']=='user_lp':
		context[ids]['data']['password']=message
		context[ids]['state']=None
		logging.debug('validating password and reseting state ')
		val=check_validity(context[ids]['data']['username'],context[ids]['data']['password'],db)
		if not val:
			send_message("Password or username incorrect",ids)
			return
		del context[ids]
		logging.debug('succesful login ')
		send_message("Succesful login", ids)

    
    
    
    
###########CONVErSATION FUNCTIONS
def check_valid_arg_plot(message):
    v1=('frequency'==message)
    v2=('series'==message)
    return v1 or v2
def token_builder(ids,db,message,typeplot):
    user=get_db_user_byid(ids,db2)
    username=user[0][0]
    password=user[0][1]
    date=1
    token={'username':username,'password':password,'date':date,'typeplot':typeplot,'data':message}
    return token    

def plot_handler(context,ids,db,message_data):
    if check_valid_arg_plot(context[ids]['state']):
        #validator here
        context[ids]['data_plot']=message_data
        token=token_builder(ids,db,message_data,context[ids]['state'])
        try:
			send_data(token)
        except:
            logging.debug("connection refused")
        if context[ids]['data_plot']=='\stop':
            print "Ending data entry"
            #send_message("Ending data entry",ids)
            del context[ids]['data_plot']
            context[ids]['state']=None
            return
        return token




def choosing_plot(context,ids,db,message):
    notkey(ids,context)
    logging.debug('INSIDE CHOOSING PLOT CONTEXT:{} MESSAGE {}'.format(context,message))
    if not context[ids]['state']:
        context[ids]['state']='choosing_plot'
        logging.debug('modifying state to choosing_plot')
        #print "choose type of plot"
        send_message("Choose type of plot series frequency",ids)
    elif context[ids]['state']=='choosing_plot':
        if check_valid_arg_plot(message):
            context[ids]['state']=message
            logging.debug('modifying state to {}'.format(message))
            #print "{} plot choosen, type \stop to stop entrying data".format(message)
            send_message("{} plot choosen, type \stop to stop entrying data".format(message),ids)
            if message=="frequency":
				send_message("Time entry format example 13:55",ids)
        else:
            #print "unknown command"
            send_message('unknown command',ids)
def conversation_plot(context,ids,db,message):
	choosing_plot(context,ids,db,message)
	token=plot_handler(context,ids,db,message)
	logger.debug('token sent {}'.format(token))


def send_data(token):
	web="http://127.0.0.1:5000/senddata"
	time=token['data']
	delta=delta_time_minutes(time)
	token['data']=delta
	r = requests.post(web,data=token)
	return r.content


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
###########################




    
    
    
    
    
    
    
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        logging.debug("update:{}".format(updates))
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            #echo_all(updates)
            #registertest(updates)
            conversation(updates)

            
            #time.sleep(0.7)
            
        

'''
def registertest(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            logging.debug("update id:{} and text{}".format(check_update_id(update),text))
            chat = update["message"]["chat"]["id"]
            if not context.has_key(chat):
				context[chat]={}
				context[chat]['state']=None            
            logging.debug("chat id:{}".format(chat))
            register(context,chat,db,text)
            logging.debug(" post register context:{}".format(context))
        except Exception as e:
            print(e)     
  
def logintest(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            logging.debug("update id:{} and text{}".format(check_update_id(update),text))
            chat = update["message"]["chat"]["id"]
            if not context.has_key(chat):
				context[chat]={}
				context[chat]['state']=None            
            logging.debug("chat id:{}".format(chat))
            login(context,chat,db,text)
            logging.debug(" post login context:{}".format(context))
        except Exception as e:
            print(e)
            
            
'''

if __name__ == '__main__':
	main()
