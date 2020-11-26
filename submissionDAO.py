from flask import Flask
from db import db
import messages
import userDAO

def save_submission(username, submission, exercise_id, verdict):
    user_id = userDAO.get_user_id(username)
    sql = "INSERT INTO submissions (user_id, submission, exercise_id, date, verdict) VALUES (:user_id, :submission, :exercise_id, NOW(), :verdict)"
    db.session.execute(sql, {"user_id":user_id, "submission":submission, "exercise_id":exercise_id, "verdict":verdict})
    db.session.commit()
    
