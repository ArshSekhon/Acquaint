from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from server import test

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
                    print(user)
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
    return render_template('dashboard.html')

@app.route("/recommendation")
def recommendation():
    x,y = test.predict_tags(1)
    print(x,y)
    print(type(x))
    return jsonify({'id': x,'id2':y})

@app.route("/recommendation/question")
def question():
    x,y = test.run_lda("I am in love")
    print(x,y)
    print(type(x))
    return jsonify({'id': x,'id2':y})

@app.route("/recommendation/url", methods=['GET'])
def url_recommendation():
    print("api working...")
    if 'url' in request.args:
        print('working')
        url = request.args['url']
    print('not working...')
    #url = request.json['url']
    print(url)
    print(type(url))
    x,y = test.read_from_url(url)
    print(x,y)
    print(type(x))
    return jsonify({'id': x,'id2':y})

if __name__ == '__main__':
    app.run(debug=True)
