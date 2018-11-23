from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from server import test

#For calling API endpoint within this app
import requests, json

#For disabling https requiremet for google authenication
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import sqlite3 as sql
import createDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This-is-swee-&-salty-key'

#For google authentication 
GOOGLE_CLIENT_ID = '164371578483-uvkhe4gn4cpnun85ge6tm72s7ddceenn.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'bFHVVUFqXrOBL0AlgEfmKKTq'
REDIRECT_URI = '/oauth2callbcak'

blueprint = make_google_blueprint(
    client_id= GOOGLE_CLIENT_ID,
    client_secret= GOOGLE_CLIENT_SECRET,
    redirect_to = 'home',
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")

#Functions
def recommendation_id_func(mid):
    print("id>>>>", mid , type(mid))
    rec_4_interest, rec_4_expert = test.predict_tags(int(mid))
    print(rec_4_expert)
    return ({'rec_4_interest': rec_4_interest,'rec_4_expert': rec_4_expert})


@app.route("/")
def index():
    return "LANDIng page"

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/home")
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        #print(resp.json())
        try:
            print("started try..")
            google_id = resp.json()["id"]
            email = resp.json()["email"]
            name = email.split("@")[0]
            print(google_id,email,name)
            with sql.connect("database.db") as con:
                print("started with..")
                cur = con.cursor()
                l = len((cur.execute('SELECT * FROM members WHERE email = ?',(email,))).fetchall())
                print(l,"<<L>>")
                if l == 0:
                    print("executing...")
                    cur.execute("INSERT INTO members (google_id, email, name) VALUES (?,?,?)",(google_id, email, name))
                    print("done... executing")
                    user = 'new'
                    con.commit()
                    msg = "Record successfully added"
                    print("DATabase executed..")
                    return redirect(url_for('new_user'))
                else:
                    user = 'existing'
                    session['email'] = email
                    return redirect(url_for('dashboard'))
            #return "You are {email} on Google".format(email=resp.json()["email"])
            #return render_template('home.html')
        except:
            con.rollback()
            msg = "error in insert operation"
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for("login"))
    return render_template('home.html')
@app.route("/new_user")
def new_user():
    return render_template('new_user.html')

@app.route("/dashboard")
def dashboard():
    try:
        print('Entered try...')
        email = session['email']
        print(email,"<<<<")
        con = sql.connect("database.db")
        cur = con.cursor()
        usr = (cur.execute('SELECT * FROM members WHERE email = ?',(email,))).fetchall()
        usr_interest = (cur.execute('SELECT * FROM interest WHERE intrst_id = ?',(usr[0][0],))).fetchall()
        usr_expertise = (cur.execute('SELECT * FROM expertise WHERE exprt_id = ?',(usr[0][0],))).fetchall()
        #print(user)
        #print(user[0][0])
    except:
        con.rollback()
        msg = "error in read operation"
    #nothing tables in yet so intialising
    usr_interest = "dummy string"
    usr_expertise = "dummy string"

    #On basis of usr_id(expterise, interest) recommended mentors/peer
    recmnd = recommendation_id_func(1)
    rec_4_interest = recmnd['rec_4_interest']
    rec_4_expert = recmnd['rec_4_expert'] 
    #print(rec_4_interest)
    
    try:
        con = sql.connect("database.db")
        cur = con.cursor()
        mentor = []
        for name in rec_4_expert:
            x = (cur.execute('SELECT name,email FROM members WHERE name = ?',(name,))).fetchall()
            print(x)
            mentor = mentor.append(x[0])
    except:
        print("error")
   
    print(type(mentor))
    context = {
        'user': {
            'usr': usr,
            'usr_interest': usr_interest,
            'usr_expertise': usr_expertise
        },
        #'interest': rec_4_interest,
        'expertise': mentor,
    }
    return render_template('dashboard.html' , context=context)



##########################
######### API's ##########
##########################
@app.route("/api/recommendation/id", methods=['GET'])
def recommendation_api():
    if 'mid' in request.args:
        mid = request.args['mid']
    print("id>>>>", mid , type(mid))
    rec_4_interest, rec_4_expert = test.predict_tags(int(mid))
    print(rec_4_expert)
    return jsonify({'rec_4_interest': rec_4_interest,'rec_4_expert': rec_4_expert})

@app.route("/api/recommendation/question", methods=['GET'])
def question_api():
    if 'ques' in request.args:
        ques = request.args['ques']
    rec_4_interest, rec_4_expert = test.run_lda(ques)
    return jsonify({'rec_4_interest': rec_4_interest,'rec_4_expert': rec_4_expert})


@app.route("/ext/processActivity", methods=['GET','POST'])
def url_recommendation():
    #print("api working...")
    print("\n\n\n\n\n\n")
    print("api working "+request.args['url'])
    print("\n\n\n\n\n\n")
    return "ok", 200, {'Access-Control-Allow-Origin': '*'}
    """if 'url' in request.args:
        #print('working')
        url = request.args['url']
    #print('not working...')
    #url = request.json['url']
    #print(url)
    #print(type(url))
    rec_4_interest, rec_4_expert = test.read_from_url(url)
    return jsonify({'rec_4_interest': rec_4_interest,'rec_4_expert': rec_4_expert})"""


@app.route("/profile_json/<i_num>")
def profile_json(i_num):
    url = "https://people.wdf.sap.corp/api/idm/users/" + str(i_num) + ".json"
    headers = {
        'Authorization': "Basic og==""",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    return response.text

@app.route("/profile/<i_num>")
def profile(i_num):
    url = "https://people.wdf.sap.corp/api/idm/users/"+str(i_num)+".json"
    headers = {
        'Authorization': "Basic og==""",
        'cache-control': "no-cache" 
        }

    #response = requests.request("GET", url, headers=headers,verify=False)

    #print(response.text)
    context = {
        'person': {
            'name': response.text['first_name'] + response.text['last_name'],
            'i_num': response.text['uid'],
            'intern_fullTime': response.text['organisation.job_family'],
        },
        'contact_info': {
            'sap_email': response.text['email'],
            'p_no': response.text['company_phone'],
            'address': response.text['street']+", "+response.text['city']+", "+response.text['country_code']+" "+response.text['zip_code'],
        },
        'org_info': {
            'office': response.text['company'],
            'org': response.text['Digital Business Services'],
            'manager': response.text['organisation.manager_uid'],
        }

    }
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
