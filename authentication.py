from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import userDAO
import messages

app.secret_key = getenv("SECRET_KEY")

@app.route("/signin")
def sign_up_form():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"].strip()
    if userDAO.invalidUsername(username):
        return render_template("register.html", username_error=messages.invalid_username())
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    if userDAO.invalidPassword(password):
        return render_template("register.html", password_error=messages.invalid_password())
    if confirm_password != password:
        return render_template("register.html", confirm_password_error=messages.mismatch_confirm_password())
    if not userDAO.create_user(username, password):
        return render_template("register.html", username_error=messages.username_taken())
    return redirect("/login")

@app.route("/login")
def get_login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
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
    if "username" in session:
        del session["username"]
    return redirect("/")

def get_logged_user():
    if "username" in session:
        return session["username"]
    else: return None

def is_admin():
    if "username" in session:
        username = session["username"]
        return userDAO.is_admin(username)
    return False
