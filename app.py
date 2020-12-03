from flask import Flask
from flask import render_template

app = Flask(__name__)

import authentication
import exercises
import submissions
import submissionDAO

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

@app.route("/leaderboard")
def leaderoard():
    leaderboard = submissionDAO.get_leaderboard()
    return render_template("leaderboard.html", leaderboard=leaderboard)

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def forbidden(e):
    return render_template('errors/405.html'), 405
