from flask import Flask
from flask import render_template, request, redirect
from app import app
import userDAO
import simulator

@app.route("/exerciselist")
def exerciselist():
    topic1 = userDAO.getExercisesByTopic(1)
    topic2 = userDAO.getExercisesByTopic(2)
    return render_template("exercises.html", topic1=topic1, topic2=topic2)

@app.route("/exercise/<int:id>")
def exercise(id):
    exercise = userDAO.getExercise(id)
    return render_template("exercise.html", id=id, heading=exercise[0], description=exercise[1], error="")

@app.route("/exercise/<int:id>", methods=["POST"])
def exercisesubmit(id):
    answer = request.form["answer"]
    isWHILEprogram = simulator.is_WHILEprogram(answer)
    if(isWHILEprogram[0]):
        commands = isWHILEprogram[1]
        variable_cnt = isWHILEprogram[2]
        tests = userDAO.getTests(id)
        tests_passed = simulator.test(commands, variable_cnt, tests)
        if tests_passed:
            return render_template("result.html", result="Onneksi olkoon, ohjelma toimii oikein!", id=id)
        else:
            return render_template("result.html", result="Ohjelma antoi väärän vastauksen.", id=id)
        return render_template("result.html", result=tests_passed, id=id)
    else:
        return render_template("result.html", result="Ohjelma ei ole WHILE-ohjelma tai se ei ole annettu oikeassa syntaksissa.", id=id)
    
@app.route("/newexercise")
def fill_in_new_exercise():
    return render_template("newexercise.html")

@app.route("/newexercise", methods=["POST"])
def submit_new_exercise():
    heading = request.form["heading"]
    if not heading:
        return render_template("newexercise.html", headingError="Otsikko ei saa olla tyhjä.")
    description = request.form["description"]
    if not description:
        return render_template("newexercise.html", descriptionError="Tehtävänanto ei saa olla tyhjä.")
    topic = request.form["topic"]
    if not topic or not topic.isnumeric():
        return render_template("newexercise.html", topicError="Aihealue pitää määritellä ja se pitää olla numero.")
    topic = int(topic)
    tests = request.form["tests"]
    create_new_exercise(heading, description, topic, tests)
    return redirect("/exerciselist")

def create_new_exercise(heading, description, topic, tests):
    exercise_id = userDAO.createNewExercise(heading, description, topic)
    lines = tests.splitlines()
    for i in range(len(lines)):
        if i%2 == 0:
            input = lines[i]
            output = int(lines[i+1])
            userDAO.createNewTest(exercise_id, input, output)
