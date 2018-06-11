
from flask import Flask, request,render_template,g,session,render_template #import main Flask class and request object
import logging
import sqlite3
import matplotlib.pyplot as plt
import mpld3
import json
from Utils2 import check_validity,insert_db_dataset,is_authentified,retrieve_db,is_authentified_session,get_db_user_data_dic,data_pack_hist
logging.basicConfig(format='\n %(asctime)s - %(name)s - %(levelname)s - %(message)s\n',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__) #create the Flask app
#to avoid csrf cross site request forgery
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

DATABASE='mydb'



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db






@app.route("/plot_test")
@is_authentified_session(session,get_db)
def plot_test():
    db=get_db()
    username=session['username']
    print username
    data_raw=get_db_user_data_dic(username,db)
    data=data_pack_hist(data_raw)
    fig=plt.figure(0)
    plt.hist(data)
    json01 = json.dumps(mpld3.fig_to_dict(fig))
    json02 = json.dumps(mpld3.fig_to_dict(fig))
    json03 = json.dumps(mpld3.fig_to_dict(fig))
    return render_template('page_mld3.html',json1=json01,json2=json02,json3=json03)










@app.route('/senddata', methods=['GET', 'POST']) #allow both GET and POST requests
@is_authentified(request,get_db)
def senddata():
	db=get_db()
	if request.method == 'POST':
		try:
			data=request.form['data']
			date=request.form['date']
			username=request.form['username']
			insert_db_dataset(date,data,username,db)
			logger.debug("Data inserted:".format(bool(data)))
		except Exception as e:
			print e
	return "successful reception"
	

##test reception
@app.route('/test_reception', methods=['GET', 'POST']) #allow both GET and POST requests
@is_authentified(request,get_db)
def test_reception():
	db=get_db()
	if request.method == 'POST':
		try:
			keys=request.form.keys()
			values=request.form.values()
			logger.debug("test_reception Data received:{}".format(values))
		except Exception as e:
			print e
	return "echo"+str(keys)+str(values)





###Test data extraction from database
@app.route('/plot_page', methods=['GET', 'POST']) #allow both GET and POST requests
@is_authentified_session(session,get_db)
def plot_page():
	db=get_db()
	username=session['username']
	logger.debug('plot_page user:{}'.format(username))
	data=get_db_user_data_dic(username,db)
	logger.debug('plot_page data:{}'.format(data))
	s=""
	for d in data:
		s="<div>{}   {}</div>".format(d['typeplot'],d['data'])+s
	return s

	

@app.route('/login', methods=['GET', 'POST']) #allow both GET and POST requests
def login():
    db=get_db()
    islog=False
    try:
        islog=session['is_logged']
        logger.debug('Login- islog value:{}'.format(islog))
    except Exception as e:
        logger.debug('Login- Not is logged in islog')
    if islog:
        return "Soon to be index/graphics"
    elif ((not islog) and request.method == 'POST'):
        username=request.form['username']
        password=request.form['password']
        isuser=bool(check_validity(username,password,db))
        if isuser:
            session['username']=username
            session['password']=password
            session['is_logged']=True
            logger.debug('stored session username and password:{}'.format(session['username'],session['password']))
        else:
            return "invalid credentials"
    return render_template('login.html')







if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
