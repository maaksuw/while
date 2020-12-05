from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

import authentication
import exercises
import submissions
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

@app.route("/profile/<string:username>")
def profile(username):
    profile = userDAO.get_profile(username)
    exercises = submissionDAO.submissions_status_for_user(username)
    return render_template("profile.html", username=username, introduction=profile[0], joined=profile[1])

@app.route("/modifyprofile/<string:username>")
def show_modify_profile(username):
    introduction = userDAO.get_profile(username)[0]
    return render_template("modifyprofile.html", username=username, current_introduction=introduction)

@app.route("/modifyprofile/<string:username>", methods=['POST'])
def modify_profile(username):
    introduction = request.form["introduction"]
    token = request.form["csrf_token"]
    if not (authentication.is_current_user(username) and authentication.correct_csrf_token(token)):
        abort(403)
    if len(introduction) < 5000:
        userDAO.update_introduction(username, introduction)
    return redirect("/profile/" + username)

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
