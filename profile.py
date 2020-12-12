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
    logged_in = authentication.get_logged_user()
    friends = False
    if logged_in != username and userDAO.are_friends(logged_in, username):
        friends = True
    return render_template("profile/profile.html", username=username, introduction=profile[0], joined=profile[1], friends=friends, topic1=topic1, topic2=topic2)

@app.route("/modifyprofile/<string:username>")
def show_modify_profile(username):
    if not authentication.is_current_user(username):
        abort(403)
    introduction = userDAO.get_profile(username)[0]
    return render_template("profile/modifyprofile.html", username=username, current_introduction=introduction)

@app.route("/modifyprofile/<string:username>", methods=['POST'])
def modify_profile(username):
    introduction = request.form["introduction"]
    token = request.form["csrf_token"]
    if not (authentication.is_current_user(username) and authentication.correct_csrf_token(token)):
        abort(403)
    if len(introduction) < 5000:
        userDAO.update_introduction(username, introduction)
    return redirect("/profile/" + username)

@app.route("/friends/<string:username>")
def friends(username):
    if authentication.get_logged_user() != username:
        abort(403)
    friends = userDAO.get_friends(username)
    return render_template("profile/friends.html", friends=friends, username=username)

@app.route("/friends/<string:username>", methods=["POST"])
def add_friends(username):
    logged_in = authentication.get_logged_user()
    if logged_in != None or not userDAO.are_friends(logged_in, username):
        userDAO.add_friends(logged_in, username)
    return redirect("/profile/" + username)

@app.route("/removefriend/<string:username>", methods=["POST"])
def delete_friend(username):
    logged_in = authentication.get_logged_user()
    if logged_in != None and userDAO.are_friends(logged_in, username):
        userDAO.delete_friends(logged_in, username)
    return redirect("/profile/" + username)
