from flask import Flask
from flask import render_template, request, redirect, abort
from app import app 

import exerciseDAO
import submissions
import authentication
import messages
    
@app.route("/exerciselist")
def list_exercises():
    admin = authentication.is_admin()
    topic1 = exerciseDAO.get_exercises_by_topic_order_by_heading(1)
    topic2 = exerciseDAO.get_exercises_by_topic_order_by_heading(2)
    return render_template("exercises/exerciselist.html", topic1=topic1, topic2=topic2, admin=admin)

@app.route("/exercise/<int:id>")
def show_exercise(id):
    exercise = exerciseDAO.get_exercise(id)
    solved = submissions.is_solved(id)
    admin = authentication.is_admin()
    return render_template("exercises/exercise.html", id=id, heading=exercise[0], solved=solved, admin=admin, description=exercise[1], error="")
    
@app.route("/newexercise")
def show_new_exercise():
    if not authentication.is_admin():
        abort(403)
    return render_template("exercises/admin/newexercise.html")
    
@app.route("/newexercise", methods=["POST"])
def submit_new_exercise():
    if not authentication.is_admin() or authentication.get_csrf_token() != request.form["csrf_token"]:
        abort(403)
    heading = request.form["heading"]
    description = request.form["description"]
    topic = request.form["topic"]
    input_size = request.form["input_size"]
    if not heading:
        return render_template("exercises/admin/newexercise.html", headingError=messages.empty_heading())
    if not description:
        return render_template("exercises/admin/newexercise.html", descriptionError=messages.empty_description())
    if not topic or not topic.isnumeric():
        return render_template("exercises/admin/newexercise.html", topicError=messages.invalid_topic())
    if not input_size or not input_size.isnumeric():
        return render_template("exercises/admin/newexercise.html", inputError=messages.invalid_input_size())
    topic = int(topic)
    input_size = int(input_size)
    create_new_exercise(heading, description, topic, input_size)
    return redirect("/exerciselist")

def create_new_exercise(heading, description, topic, input_size):
    exercise_id = exerciseDAO.create_exercise(heading, description, topic, input_size)

@app.route("/modifyexercise/<int:id>")
def show_modify_exercise(id):
    if not authentication.is_admin():
        abort(403)
    exercise = exerciseDAO.get_exercise(id)
    return render_template("exercises/admin/modifyexercise.html", id=id, current_heading=exercise[0], current_description=exercise[1], current_topic=exercise[2], current_input_size=exercise[3])

@app.route("/modifyexercise/<int:id>", methods=["POST"])
def modify_exercise(id):
    if not authentication.is_admin() or authentication.get_csrf_token() != request.form["csrf_token"]:
        abort(403)
    heading = request.form["heading"]
    description = request.form["description"]
    topic = request.form["topic"]
    input_size = request.form["input_size"]
    if not heading:
        return render_template("exercises/admin/modifyexercise.html", headingError=messages.empty_heading(), id=id)
    if not description:
        return render_template("exercises/admin/modifyexercise.html", descriptionError=messages.empty_description(), id=id)
    if not topic or not topic.isnumeric():
        return render_template("exercises/admin/modifyexercise.html", topicError=messages.invalid_topic(), id=id)
    if not input_size or not input_size.isnumeric():
        return render_template("exercises/admin/modifyexercise.html", inputError=messages.invalid_input_size(), id=id)
    topic = int(topic)
    input_size = int(input_size)
    exerciseDAO.update_exercise(heading, description, topic, input_size, id)
    return redirect("/exercise/" + str(id))

@app.route("/modifyexercise/<int:id>/tests")
def list_tests(id):
    if not authentication.is_admin():
        abort(403)
    heading = exerciseDAO.get_heading(id)
    tests = exerciseDAO.get_tests(id)
    return render_template("exercises/admin/modifytests.html", heading=heading, id=id, tests=tests)

@app.route("/modifyexercise/<int:id>/tests", methods=["POST"])
def modify_test(id):
    if not authentication.is_admin() or authentication.get_csrf_token() != request.form["csrf_token"]:
        abort(403)
    input = request.form["input"]
    output = request.form["output"]
    if request.form["modbutton"] == "modify":
        test_id = request.form["id"]
        input_size = exerciseDAO.get_input_size(id)
        if messages.input_formatter().fullmatch(input) and len(input.split()) == input_size and output.isnumeric():
            exerciseDAO.update_test(input, output, test_id)
    elif request.form["modbutton"] == "delete":
        test_id = request.form["id"]
        exerciseDAO.remove_test(test_id)
    elif request.form["modbutton"] == "new":
        input_size = exerciseDAO.get_input_size(id)
        create_new_test(id, input, output, input_size)
    return redirect("/modifyexercise/" + str(id) + "/tests")

def create_new_test(exercise_id, input, output, input_size):
    if messages.input_formatter().fullmatch(input) and output.isnumeric() and len(input.split()) == input_size:
        output = int(output)
        exerciseDAO.create_test(exercise_id, input, output)
        
