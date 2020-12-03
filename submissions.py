from flask import Flask
from flask import render_template, request, redirect, abort
from app import app
import exerciseDAO
import submissionDAO
import authentication
import parser
import simulator
import messages

@app.route("/exercise/<int:id>", methods=["POST"])
def submit_exercise(id):
    submission = request.form["answer"]
    print(len(submission))
    if len(submission) > 100000:
        result = messages.wrong_answer()
        message = messages.long_submission()
        solved = is_solved(id)
        heading = exerciseDAO.get_heading(id)
        admin = authentication.is_admin()
        return render_template("exercises/unsuccessful.html", result=result, message=message, id=id, solved=solved, heading=heading, admin=admin)
    input_size = exerciseDAO.get_input_size(id)
    isWHILEprogram = parser.is_WHILEprogram(submission, input_size)
    if(isWHILEprogram[0]):
        return handle_testing(submission, isWHILEprogram, id)
    else:
        return handle_parse_error(isWHILEprogram, id)
    
def handle_testing(submission, parsed_program, id):
    heading = exerciseDAO.get_heading(id)
    commands = parsed_program[1]
    variable_cnt = parsed_program[2]
    tests = exerciseDAO.get_tests(id)
    tests_passed = simulator.test(commands, variable_cnt, tests)
    if tests_passed == True:
        #Successful submission OK
        save_submission(submission, id, "OK")
        return redirect("/comments/" + str(id) + "/congratulations")
    else:
        solved = is_solved(id)
        admin = authentication.is_admin()
        result=messages.wrong_answer()
        message = ""
        if tests_passed[0] == 1:
            #Steplimit exceeded SE
            save_submission(submission, id, "SE")
            message = messages.steplimit_exceeded()
        elif tests_passed[0] == 2:
            #Wrong answer WA
            save_submission(submission, id, "WA")
            input = tests_passed[1]
            correct_output = tests_passed[2]
            user_output = tests_passed[3]
            message = messages.explain_incorrect_answer(input, str(user_output), str(correct_output))
        return render_template("exercises/unsuccessful.html", result=result, message=message, id=id, solved=solved, heading=heading, admin=admin)
    
def handle_parse_error(what_went_wrong, id):
    heading = exerciseDAO.get_heading(id)
    solved = is_solved(id)
    admin = authentication.is_admin()
    error = what_went_wrong[1]
    message = ""
    result = messages.not_WHILEprogram()
    if error != messages.bracket_missing() and error != messages.wrong_input_size():
        message = "Seuraava rivi antoi virheen.\n"
    message += error
    return render_template("exercises/unsuccessful.html", result=result, message=message, id=id, solved=solved, heading=heading, admin=admin)

def save_submission(submission, exercise_id, verdict):
    username = authentication.get_logged_user()
    if username != None:
        submissionDAO.save_submission(username, submission, exercise_id, verdict)
    
def is_solved(id):
    username = authentication.get_logged_user()
    if username == None:
        return False
    return submissionDAO.is_exercise_solved(username, id)
    
@app.route("/submissions/<int:id>")
def show_submissions(id):
    heading = exerciseDAO.get_heading(id)
    solved = is_solved(id)
    admin = authentication.is_admin()
    username = authentication.get_logged_user()
    if username == None:
        abort(403)
    submissions = submissionDAO.get_submissions_by_user_id_and_exercise_id(username, id)
    return render_template("exercises/submissions.html", id=id, heading=heading, solved=solved, admin=admin, submissions=submissions)

@app.route("/comments/<int:id>/<string:message>")
def show_comments(id, message):
    solved = is_solved(id)
    admin = authentication.is_admin()
    if authentication.get_logged_user == None or (not solved and not admin):
        abort(403)
    heading = exerciseDAO.get_heading(id)
    successful_submissions = submissionDAO.get_successful_submissions_count(id)
    all_submissions = submissionDAO.get_all_submissions_count(id)
    newest_submission_date = submissionDAO.get_newest_submission_time(id)
    comments = submissionDAO.get_comments(id)
    if message != "normal":
        return render_template("exercises/after.html", id=id, heading=heading, solved=solved, admin=admin, successful_submissions=successful_submissions, all_submissions=all_submissions, newest_submission_date=newest_submission_date, comments=comments, message=messages.successful_submission())
    return render_template("exercises/after.html", id=id, solved=solved, heading=heading, successful_submissions=successful_submissions, all_submissions=all_submissions, newest_submission_date=newest_submission_date, comments=comments, admin=admin)

@app.route("/comments/<int:id>", methods=["POST"])
def post_comment(id):
    username = authentication.get_logged_user()
    comment = request.form["comment"]
    if len(comment) > 10000:
        return redirect("/comments/" + str(id) + "/normal")
    submissionDAO.post_comment(username, comment, id)
    return redirect("/comments/" + str(id) + "/normal")

@app.route("/submissions/<int:id>/all")
def show_all_submissions(id):
    heading = exerciseDAO.get_heading(id)
    solved = is_solved(id)
    admin = authentication.is_admin()
    username = authentication.get_logged_user()
    if username == None or not admin:
        abort(403)
    submissions = submissionDAO.get_submissions_by_exercise_id(id)
    return render_template("exercises/submissions.html", id=id, heading=heading, solved=solved, admin=admin, submissions=submissions)
