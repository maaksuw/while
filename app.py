from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/basics")
def basics():
    return render_template("basics.html")

# Autentikaatiot

@app.route("/signin")
def signinget():
    return render_template("register.html", error="")

@app.route("/register", methods=["POST"])
def signinpost():
    username = request.form["username"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    else:
        return render_template("register.html", error="Käyttäjänimi on jo varattu.")
    return redirect("/")

@app.route("/login")
def loginget():
    return render_template("login.html", usernameError="", passwordError="")

@app.route("/login", methods=["POST"])
def loginpost():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        # TODO: invalid username
        return render_template("login.html", usernameError="Käyttäjänimi on väärin.")
    else:
        hash_value = user[0]
        if not check_password_hash(hash_value,password):
            return render_template("login.html", passwordError="Salasana on väärin.")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# Tehtävät

@app.route("/exercises")
def exercises():
    return render_template("exercises.html")

@app.route("/exercise1")
def exercise1():
    return render_template("exercise1.html")

@app.route("/exercise2")
def exercise2():
    return render_template("exercise2.html")

@app.route("/exercise3")
def exercise3():
    return render_template("exercise3.html")
