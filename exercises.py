from flask import Flask
from flask import render_template, request, redirect
from app import app
import userDAO
import simulator

@app.route("/exerciselist")
def exerciselist():
    topic1 = userDAO.getExercisesByTopic(1)
    for t in topic1:
        print(t)
    topic2 = userDAO.getExercisesByTopic(2)
    for t in topic2:
        print(t)
    return render_template("exercises.html", topic1=topic1, topic2=topic2)

@app.route("/exercise/<int:id>")
def exercise(id):
    exercise = userDAO.getExercise(id)
    return render_template("exercise.html", id=id, heading=exercise[0], description=exercise[1])

@app.route("/exercise/<int:id>", methods=["POST"])
def exercisesubmit(id):
    answer = request.form["answer"]
    #Käsittele vastaus täällä!
    simulator.parse(answer)
    return "jotain"
