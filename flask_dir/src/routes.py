from flask import Flask, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google

#For disabling https requiremet for google authenication
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    #return "You are {email} on Google".format(email=resp.json()["email"])
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
