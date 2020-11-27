from flask import Flask
from flask import render_template, request, redirect
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
    isWHILEprogram = parser.is_WHILEprogram(submission)
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
        solved = get_solved(id)
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
        return render_template("exercises/unsuccessful.html", result=result, message=message, id=id, solved=solved, heading=heading)
    
def handle_parse_error(what_went_wrong, id):
    heading = exerciseDAO.get_heading(id)
    solved = get_solved(id)
    error = what_went_wrong[1]
    message = ""
    result = messages.not_WHILEprogram()
    if error != messages.bracket_missing():
        message = "Seuraava rivi antoi virheen.\n"
    message += error
    return render_template("exercises/unsuccessful.html", result=result, message=message, id=id, solved=solved, heading=heading)

def save_submission(submission, exercise_id, verdict):
    session = authentication.get_session()
    submissionDAO.save_submission(session["username"], submission, exercise_id, verdict)
    
def get_solved(id):
    username = get_username()
    if username == None:
        return False
    return submissionDAO.is_exercise_solved(username, id)

def get_username():
    session = authentication.get_session()
    if "username" in session:
        return session["username"]
    return None
    
@app.route("/submissions/<int:id>")
def show_submissions(id):
    heading = exerciseDAO.get_heading(id)
    solved = get_solved(id)
    username = get_username()
    submissions = submissionDAO.get_submissions_by_user_id_and_exercise_id(username, id)
    return render_template("exercises/submissions.html", id=id, submissions=submissions, solved=solved, heading=heading)

@app.route("/comments/<int:id>/<string:message>")
def show_comments(id, message):
    heading = exerciseDAO.get_heading(id)
    solved = get_solved(id)
    successful_submissions = submissionDAO.get_successful_submissions_count(id)
    all_submissions = submissionDAO.get_all_submissions_count(id)
    newest_submission_date = submissionDAO.get_newest_submission_time(id)
    comments = submissionDAO.get_comments(id)
    if message != "normal":
        return render_template("exercises/after.html", id=id, solved=solved, heading=heading, successful_submissions=successful_submissions, all_submissions=all_submissions, newest_submission_date=newest_submission_date, comments=comments, message=messages.successful_submission())
    return render_template("exercises/after.html", id=id, solved=solved, heading=heading, successful_submissions=successful_submissions, all_submissions=all_submissions, newest_submission_date=newest_submission_date, comments=comments)

@app.route("/comments/<int:id>", methods=["POST"])
def post_comment(id):
    username = get_username()
    comment = request.form["comment"]
    submissionDAO.post_comment(username, comment, id)
    return redirect("/comments/" + str(id) + "/normal")
