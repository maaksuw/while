from flask import Flask
from flask import render_template, request
from app import app
import userDAO
import parser
import simulator
import messages

@app.route("/exercise/<int:id>", methods=["POST"])
def submit_exercise(id):
    submission = request.form["answer"]
    isWHILEprogram = parser.is_WHILEprogram(submission)
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
            message = messages.steplimit_exceeded()
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
