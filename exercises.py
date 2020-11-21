from flask import Flask
from flask import render_template, request, redirect
from app import app
import userDAO
import simulator
import messages

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
        return handle_testing(isWHILEprogram, id)
    else:
        return handle_parse_error(isWHILEprogram, id)
    
def handle_testing(parsed_program, id):
    commands = parsed_program[1]
    variable_cnt = parsed_program[2]
    tests = userDAO.getTests(id)
    tests_passed = simulator.test(commands, variable_cnt, tests)
    if tests_passed == True:
        return render_template("result.html", result=messages.successful_submission(), id=id)
    else:
        result=messages.wrong_answer()
        message = ""
        if tests_passed[0] == 1:
            message = tests_passed[1]
        elif tests_passed[0] == 2:
            input = tests_passed[1]
            correct_output = tests_passed[2]
            user_output = tests_passed[3]
            message = messages.explain_incorrect_answer(input, str(user_output), str(correct_output))
        return render_template("result.html", result=result, message=message, id=id)
    
def handle_parse_error(what_went_wrong, id):
    error = what_went_wrong[1]
    message = ""
    result = messages.not_WHILEprogram()
    if error != messages.bracket_missing():
        message = "Seuraava rivi antoi virheen.\n"
    message += error
    return render_template("result.html", result=result, message=message, id=id)
    
@app.route("/newexercise")
def fill_in_new_exercise():
    return render_template("newexercise.html")

@app.route("/newexercise", methods=["POST"])
def submit_new_exercise():
    heading = request.form["heading"]
    description = request.form["description"]
    topic = request.form["topic"]
    if not heading:
        return render_template("newexercise.html", headingError=messages.empty_heading())
    if not description:
        return render_template("newexercise.html", descriptionError=messages.empty_description())
    if not topic or not topic.isnumeric():
        return render_template("newexercise.html", topicError=messages.invalid_topic())
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

@app.route("/modifyexercise/<int:id>")
def modify_exercise(id):
    exercise = userDAO.getExercise(id) 
    return render_template("modifyexercise.html", id=id, current_heading=exercise[0], current_description=exercise[1], current_topic=exercise[2])

@app.route("/modifyexercise/<int:id>", methods=["POST"])
def modify_exercise2(id):
    heading = request.form["heading"]
    description = request.form["description"]
    topic = request.form["topic"]
    if not heading:
        return render_template("modifyexercise.html", headingError=messages.empty_heading(), id=id)
    if not description:
        return render_template("modifyexercise.html", descriptionError=messages.empty_description(), id=id)
    if not topic or not topic.isnumeric():
        return render_template("modifyexercise.html", topicError=messages.invalid_topic(), id=id)
    topic = int(topic)
    userDAO.update_exercise(heading, description, topic, id)
    return redirect("/exercise/" + str(id))
