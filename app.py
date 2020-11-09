from flask import Flask
from flask import render_template

app = Flask(__name__)

import authentication
import exercises

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/basics")
def basics():
    return render_template("basics.html")

@app.route("/profile/<string:username>")
def profile(username):
    return render_template("profile.html", username=username)

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")
