from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import userDAO

app.secret_key = getenv("SECRET_KEY")

@app.route("/signin")
def signinget():
    return render_template("register.html", error="")

@app.route("/register", methods=["POST"])
def signinpost():
    username = request.form["username"]
    if userDAO.invalidUsername(username):
        return render_template("register.html", usernameError="Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä.")
    password = request.form["password"]
    if userDAO.invalidPassword(password):
        return render_template("register.html", passwordError="Salasanan tulee olla vähintään 8 merkkiä pitkä ja siinä saa käyttää suomalaisen aakkoston isoja ja pieniä kirjaimia. Salasanassa pitää olla vähintään yksi numero.")
    if not userDAO.createNewUser(username, password):
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


