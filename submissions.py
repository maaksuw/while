from flask import Flask
from flask import render_template, request, redirect, abort
from app import app
import os
import exerciseDAO
import submissionDAO
import authentication
import parser
import simulator
import messages
import io

app.config['MAX_CONTENT_LENGTH'] = 1024 * 500
app.config['UPLOAD_EXTENSIONS'] = ['.while']

@app.route("/exercise/<int:id>", methods=["POST"])
def submit_exercise(id):
    token = request.form["csrf_token"]
    if not (authentication.user_is_logged_in() and authentication.correct_csrf_token(token)):
        abort(403)
    submission = request.form["answer"]
    if len(submission) > 100000:
        return inproper_submission(id, messages.long_submission())
    if submission != "":
        print(submission)
        return handle_text_submission(id, submission)
    else:
        file = request.files["answer_file"]
        return handle_file_submission(id, file)
            
def handle_file_submission(id, file):
    if file.filename != "":
        extension = os.path.splitext(file.filename)[1]
        if extension not in app.config['UPLOAD_EXTENSIONS']:
            return inproper_submission(id, messages.wrong_file_extension())
        else:
            submission = file.getvalue().decode("utf-8")
            if len(submission) > 100000:
                return inproper_submission(id, messages.long_submission())
            return handle_text_submission(id, submission)
    else:
        return redirect("/exercise/" + str(id))
            
def handle_text_submission(id, submission):
    input_size = exerciseDAO.get_input_size(id)
    result = parser.is_WHILEprogram(submission, input_size)
    if(result[0]):
        return handle_testing(submission, result, id)
    else:
        return handle_parse_error(result, id)
    
def handle_testing(submission, parsed_program, id):
    commands = parsed_program[1]
    variable_cnt = parsed_program[2]
    tests = exerciseDAO.get_tests(id)
    tests_passed = simulator.test(commands, variable_cnt, tests)
    if tests_passed == True:
        save_submission(submission, id, "OK")
        return redirect("/comments/" + str(id) + "/congratulations")
    else:
        if tests_passed[0] == 1:
            return wrong_answer(id, messages.steplimit_exceeded(), submission, "SE")
        elif tests_passed[0] == 2:
            input = result[1]
            user_output = result[3]
            correct_output = result[2]
            message = messages.explain_incorrect_answer(input, str(user_output), str(correct_output))
            return wrong_answer(id, message, submission, "WA")
    
def handle_parse_error(error, id):
    menu = get_menu_info(id)
    error_msg = error[1]
    result = messages.not_WHILEprogram()
    message = ""
    if error_msg == messages.bracket_missing() or error_msg == messages.wrong_input_size():
        message = error_msg
    else:
        message = "Seuraava rivi antoi virheen.\n"+ error_msg
    return render_template("exercises/unsuccessful.html", id=id, heading=menu[0], solved=menu[1], admin=menu[2], result=result, message=message)

def wrong_answer(id, message, submission, verdict):
    menu = get_menu_info(id)
    result = messages.wrong_answer()
    message = message
    save_submission(submission, id, verdict)
    return render_template("exercises/unsuccessful.html", id=id, heading=menu[0], solved=menu[1], admin=menu[2], result=result, message=message)

def inproper_submission(id, message):
    menu = get_menu_info(id)
    result = messages.inproper_submission()
    message = message
    return render_template("exercises/unsuccessful.html",  id=id, heading=menu[0], solved=menu[1], admin=menu[2], result=result, message=message)

def get_menu_info(id):
    heading = exerciseDAO.get_heading(id)
    solved = is_solved(id)
    admin = authentication.is_admin()
    return (heading, solved, admin)

def save_submission(submission, exercise_id, verdict):
    username = authentication.get_logged_user()
    submissionDAO.save_submission(username, submission, exercise_id, verdict)
    
def is_solved(id):
    username = authentication.get_logged_user()
    if username == None:
        return False
    return submissionDAO.is_exercise_solved(username, id)
    
@app.route("/submissions/<int:id>")
def show_submissions(id):
    if not authentication.user_is_logged_in():
        return redirect("/login")
    menu = get_menu_info(id)
    username = authentication.get_logged_user()
    submissions = submissionDAO.get_submissions_by_user_id_and_exercise_id(username, id)
    return render_template("exercises/submissions.html", id=id, heading=menu[0], solved=menu[1], admin=menu[2], submissions=submissions)

@app.route("/comments/<int:id>/<string:message>")
def show_comments(id, message):
    if not authentication.user_is_logged_in():
        return redirect("/login")
    menu = get_menu_info(id)
    if not(menu[1] or menu[2]): #menu[1] = solved, menu[2] = admin
        abort(403)
    ratio = submissionDAO.get_success_ratio(id)
    date = submissionDAO.get_newest_submission_time(id)
    comments = submissionDAO.get_comments(id)
    sign = ""
    if message == "congratulations":
        sign = messages.successful_submission()
    return render_template("exercises/after.html", id=id, heading=menu[0], solved=menu[1], admin=menu[2], message=sign, ratio=ratio, newest_submission_date=date, comments=comments)

@app.route("/comments/<int:id>", methods=["POST"])
def post_comment(id):
    token = request.form["csrf_token"]
    if not (authentication.user_is_logged_in() and authentication.correct_csrf_token(token)):
        abort(403)
    if not(is_solved or authentication.is_admin()):
        abort(403)
    username = authentication.get_logged_user()
    comment = request.form["comment"]
    if len(comment) <= 10000:
        submissionDAO.post_comment(username, comment, id)
    return redirect("/comments/" + str(id) + "/ok")

@app.route("/submissions/<int:id>/all")
def show_all_submissions(id):
    if not authentication.is_admin():
        abort(403)
    menu = get_menu_info(id)
    username = authentication.get_logged_user()
    submissions = submissionDAO.get_submissions_by_exercise_id(id)
    return render_template("exercises/submissions.html", id=id, heading=menu[0], solved=menu[1], admin=menu[2], submissions=submissions)
