import sqlite3
import hashlib
import logging
from functools import wraps
logging.basicConfig(format='\n %(asctime)s - %(name)s - %(levelname)s - %(message)s\n',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def insert_db_users(ids,username,password,db):
	cursor=db.cursor()
	password_hash=hashlib.sha224(bytes(password)).hexdigest()
	cursor.execute('''INSERT INTO users(ids,username,password)
                  VALUES(?,?,?)''', (ids,username,password_hash))
	db.commit()

def insert_db_users_nonhashed(ids,username,password,db):
	cursor=db.cursor()
	cursor.execute('''INSERT INTO users(ids,username,password)
                  VALUES(?,?,?)''', (ids,username,password))
	db.commit()


def insert_db_dataset(date,data,datasetuser,db):
	cursor=db.cursor()
	ids=get_db_users_id(datasetuser,db)
	if ids:
		cursor.execute('''INSERT INTO dataset(date,data,datasetuser,count)
					VALUES(?,?,?,?)''', (date,data,ids,1))
		logger.debug("Data inserted into user of id:".format(ids))
		db.commit()
	else:
		logger.debug("User not found ids:".format(ids))



def insert_db_dataset_token(token,db):
	cursor=db.cursor()
	username=token['username']
	ids=get_db_users_id(username,db)
	date=token['date']
	data=token['data']
	typeplot=token['typeplot']
	if ids:
		cursor.execute('''INSERT INTO dataset(date,data,datasetuser,typeplot,count)
					VALUES(?,?,?,?,?)''', (date,data,ids,typeplot,1))
		logger.debug("Data inserted into user of id:{}".format(ids))
		db.commit()
	else:
		logger.debug("User not found ids:".format(ids))


def get_db_users_id(username,db):
	cursor=db.cursor()
	cursor.execute('''SELECT id,username FROM users WHERE username=? ''',(username,))
	ids=cursor.fetchall()
	if ids:
		return ids[0][0]

def get_db_user_data(username,db):
	cursor=db.cursor()
	ids=get_db_users_id(username,db)
	cursor.execute('''SELECT * FROM dataset WHERE datasetuser=? ''',(ids,))
	data=cursor.fetchall()
	return data

#returns data as dictionary
def get_db_user_data_dic(username,db):
    cursor=db.cursor()
    cursor.execute('''SELECT * FROM dataset''')
    names = tuple(map(lambda x: x[0], cursor.description))
    data=get_db_user_data(username,db)
    datadic=map(lambda x: dict(zip(names,x)),data)
    return datadic





def get_db_user_byid(ids,db):
	cursor=db.cursor()
	cursor.execute('''SELECT username,password FROM users WHERE ids=?''',(ids,))
	user=cursor.fetchall()
	return user

def delete_db_users(username,db):
	cursor=db.cursor()
	#first we delete the rows in tables with foreign key constraint to users id
	ids=get_db_users_id(username,db)
	logger.debug("user to delete{}:".format(ids))
	datasetuser=ids
	cursor.execute('''DELETE FROM dataset WHERE datasetuser=?''',(datasetuser,))
	cursor.execute('''DELETE FROM USERS WHERE username=?''',(username,))
	logger.debug("Succesful delete of user {}".format(ids))
	db.commit()

	
def retrieve_db(db):
	cursor=db.cursor()
	cursor.execute('''SELECT * FROM users''')
	a1=cursor.fetchall()
	cursor.execute('''SELECT * FROM dataset''')
	a2=cursor.fetchall()
	return a1,a2

def check_validity(username,password,db):
	cursor=db.cursor()
	password_hash=hashlib.sha224(bytes(password)).hexdigest()
	cursor.execute('''SELECT username, password FROM users WHERE username=? AND password=?''',(username,password_hash))
	return cursor.fetchall()

def check_id_exist(ids,db):
	cursor=db.cursor()
	cursor.execute('''SELECT username, password FROM users WHERE ids=?''',(ids,))
	return cursor.fetchall()
	
def check_user_exists(username,db):
	cursor=db.cursor()
	cursor.execute('''SELECT username FROM users WHERE username=?''',(username,))
	return cursor.fetchall()
#convert string to float and return ready to plot hist data
def data_pack_hist(data_raw):
    data=[]
    for d in data_raw:
        try:
            value=float(d['data'])
            data.append(value)
        except ValueError:
            pass
    return data



#Return true if the token contains the login credentials only for non session users
def is_authentified(request,dbs):
    def decorator(f):
        #wraps preserve the name of the decorated function
        @wraps(f)
        def decorated_function(*args,**kwargs):
            db=dbs()
            username=request.form['username']
            password=request.form['password']
            isuser=check_validity(username,password,db)
            logger.debug("user authentified {}".format(bool(isuser)))
            if not isuser:
                print "NOT AUTHENTIFIED"
                return "login please"
            return f(*args,**kwargs)
        return decorated_function
    return decorator


def is_authentified_session(session,dbs):
    def decorator(f):
        #wraps preserve the name of the decorated function
        @wraps(f)
        def decorated_function(*args,**kwargs):
            db=dbs()
            if ('username' in session) and ('password' in session):                
                isuser=bool(check_validity(session['username'],session['password'],db))
                logger.debug('is_authentified_session user found:{}'.format(isuser))
                if not isuser:
                    return "Login please"
            else:
				return "login please"
            return f(*args,**kwargs)
        return decorated_function
    return decorator


	
