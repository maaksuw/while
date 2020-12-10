from flask import Flask
from flask import render_template, request, redirect, abort

app = Flask(__name__)

import exercises
import submissions
import profile

import submissionDAO
import userDAO
import messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/basics")
def basics():
    return render_template("basics.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/leaderboard")
def leaderoard():
    leaderboard = submissionDAO.get_leaderboard()
    return render_template("leaderboard.html", leaderboard=leaderboard)

@app.route("/search", methods=['GET'])
def search():
    username = request.args["keyword"]
    if len(username) > 100:
        return render_template("notfound.html", message=messages.user_not_found())
    actual_username = userDAO.existing_user(username)
    if actual_username:
        return redirect("/profile/" + username)
    return render_template("notfound.html", message=messages.user_not_found())

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def forbidden(e):
    return render_template('errors/405.html'), 405
