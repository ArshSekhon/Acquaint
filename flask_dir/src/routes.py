from flask import Flask, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError

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
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")

'''
@app.route("/")
def index():
    return "LANDIng page"
'''
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        #print(resp.json())
        try:
            google_id = resp.json()["id"]
            email = resp.json()["email"]
            name = email.split("@")[0]
            with sql.connect("database.db") as con:
                cur = con.cursor()
                l = len((cur.execute('SELECT * FROM members WHERE email = ?',(email,))).fetchall())
                if l == 0:
                    cur.execute("INSERT INTO member (google_id, email, name) VALUES (?,?)",(google_id, email, name))
                    user = 'new'
                    con.commit()
                    msg = "Record successfully added"
                    return redirect(url_for('new_user'))
                else:
                    user = 'existing'
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

if __name__ == '__main__':
    app.run(debug=True)
