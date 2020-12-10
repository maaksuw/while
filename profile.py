from flask import Flask
from flask import render_template, request, redirect, abort
from app import app

import authentication
import exerciseDAO
import userDAO

@app.route("/profile/<string:username>")
def profile(username):
    profile = userDAO.get_profile(username)
    topic1 = exerciseDAO.get_exercises_by_topic_in_order(1, username)
    topic2 = exerciseDAO.get_exercises_by_topic_in_order(2, username)
    return render_template("profile.html", username=username, introduction=profile[0], joined=profile[1], topic1=topic1, topic2=topic2)

@app.route("/modifyprofile/<string:username>")
def show_modify_profile(username):
    if not authentication.is_current_user(username):
        abort(403)
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
