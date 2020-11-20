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
        if tests_passed == True:
            return render_template("result.html", result="Onneksi olkoon, ohjelma toimii oikein!", id=id)
        else:
            input = tests_passed[0]
            correct_output = tests_passed[1]
            user_output = tests_passed[2]
            result="Ohjelma antoi väärän vastauksen."
            message = []
            message.append("Ohjelmasi antoi syötteellä " + input + " tuloksen " + str(user_output) + ".")
            message.append("Oikea tulos oli " + str(correct_output) + ".")
            return render_template("result.html", result=result, message=message, id=id)
    else:
        error_cmd = isWHILEprogram[1]
        message = []
        result = "Ohjelma ei ole WHILE-ohjelma tai se ei ole annettu oikeassa syntaksissa." 
        if error_cmd != "Kaarisulje puuttuu.":
            message.append("Seuraava rivi antoi virheen. ")
        message.append(error_cmd)
        return render_template("result.html", result=result, message=message, id=id)
    
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
