from flask import Flask
from flask import render_template
from app import app

@app.route("/exercises")
def exercises():
    return render_template("exercises/exercises.html")

@app.route("/exercise1")
def exercise1():
    return render_template("exercises/exercise1.html")

@app.route("/exercise2")
def exercise2():
    return render_template("exercises/exercise2.html")

@app.route("/exercise3")
def exercise3():
    return render_template("exercises/exercise3.html")

@app.route("/exercise4")
def exercise4():
    return render_template("exercises/exercise4.html")

@app.route("/exercise5")
def exercise5():
    return render_template("exercises/exercise5.html")

@app.route("/exercise6")
def exercise6():
    return render_template("exercises/exercise6.html")

@app.route("/exercise7")
def exercise7():
    return render_template("exercises/exercise7.html")

@app.route("/exercise8")
def exercise8():
    return render_template("exercises/exercise8.html")

@app.route("/exercise9")
def exercise9():
    return render_template("exercises/exercise9.html")

@app.route("/exercise10")
def exercise10():
    return render_template("exercises/exercise10.html")
