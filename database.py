import sqlite3

db = sqlite3.connect('mydb')
db2 = sqlite3.connect('mydb_nonhashed')
cursor2=db2.cursor()
# Get a cursor object
cursor = db.cursor()
###EXAMPLE
#try:
#	cursor.execute('''
#		CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
#						phone TEXT, email TEXT unique, password TEXT)
#	''')
#	db.commit()
#except:
#	print "table already exist baby"
#	
#	
#cursor = db.cursor()
#name1 = 'Andres'
#phone1 = '3366858'
#email1 = 'user@example.com'
## A very secure password
#password1 = '12345'
#cursor.execute('''INSERT INTO users(name, phone, email, password)
#                  VALUES(?,?,?,?)''', (name1,phone1, email1, password1))
       
#db.commit()
''' One to many example
CREATE TABLE artist(
  artistid    INTEGER PRIMARY KEY, 
  artistname  TEXT
);

CREATE TABLE track(
  trackid     INTEGER, 
  trackname   TEXT, 
  trackartist INTEGER,
  FOREIGN KEY(trackartist) REFERENCES artist(artistid)
);
'''
try:
	cursor.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY,ids TEXT unique, username TEXT,password TEXT)''')
	cursor.execute('''CREATE TABLE dataset(dataid INTEGER,date INTEGER,data TEXT,count INTEGER,datasetuser INTEGER,FOREIGN KEY(datasetuser) REFERENCES users(id))''')
	db.commit()
except Exception as e:
	print e
	

try:
	cursor2.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY,ids TEXT unique, username TEXT,password TEXT)''')
	db2.commit()
except Exception as e:
	print e
	

try:
	cursor.execute('''ALTER TABLE dataset ADD COLUMN typeplot TEXT;''')
except Exception as e:
	print e

#ids="324242424242"
#username="shit"
#password="1234"
#cursor.execute('''INSERT INTO users(ids,username,password)
#                  VALUES(?,?,?)''', (ids,username,password))
#db.commit()

