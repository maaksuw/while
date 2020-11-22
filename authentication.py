from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import userDAO
import messages

app.secret_key = getenv("SECRET_KEY")

@app.route("/signin")
def signinget():
    return render_template("register.html", error="")

@app.route("/register", methods=["POST"])
def signinpost():
    username = request.form["username"]
    if userDAO.invalidUsername(username):
        return render_template("register.html", usernameError=messages.invalid_username())
    password = request.form["password"]
    if userDAO.invalidPassword(password):
        return render_template("register.html", passwordError=messages.invalid_password())
    if not userDAO.create_user(username, password):
        return render_template("register.html", usernameError=messages.username_taken())
    return redirect("/login")

@app.route("/login")
def loginget():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginpost():
    username = request.form["username"]
    password = request.form["password"]  
    actualPassword = userDAO.get_password(username)
    if actualPassword == None:
        return render_template("login.html", error=messages.wrong_credentials())
    else:
        hash_value = actualPassword[0]
        if not check_password_hash(hash_value, password):
            return render_template("login.html", error=messages.wrong_credentials())
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
