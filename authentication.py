from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import userDAO
import re

app.secret_key = getenv("SECRET_KEY")

@app.route("/signin")
def signinget():
    return render_template("register.html", error="")

@app.route("/register", methods=["POST"])
def signinpost():
    username = request.form["username"]
    if invalidUsername(username):
        return render_template("register.html", usernameError="Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä.")
    if userDAO.getPassword(username) == None:
        password = request.form["password"]
        if invalidPassword(password):
            return render_template("register.html", passwordError="Salasanan tulee olla vähintään 8 merkkiä pitkä ja siinä saa käyttää suomalaisen aakkoston isoja ja pieniä kirjaimia. Salasanassa pitää olla vähintään yksi numero.")
        userDAO.createNewUser(username, password)
    else:
        return render_template("register.html", usernameError="Käyttäjänimi on jo varattu.")
    return redirect("/login")

@app.route("/login")
def loginget():
    return render_template("login.html", usernameError="", passwordError="")

@app.route("/login", methods=["POST"])
def loginpost():
    username = request.form["username"]
    password = request.form["password"]  
    actualPassword = userDAO.getPassword(username)
    if actualPassword == None:
        return render_template("login.html", usernameError="Käyttäjänimi on väärin.")
    else:
        hash_value = actualPassword[0]
        if not check_password_hash(hash_value, password):
            return render_template("login.html", passwordError="Salasana on väärin.")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

def invalidUsername(username):
    if len(username) < 3: return True
    return False

def invalidPassword(password):
    if len(password) < 8: return True
    regex = re.compile("([a-zA-Z]|[öäå]|[ÖÄÅ])*[0-9]([a-zA-Z]|[öäå]|[ÖÄÅ]|[0-9])*")
    if regex.fullmatch(password) == None: return True
    return False
