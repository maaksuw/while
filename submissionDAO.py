from flask import Flask
from db import db
import messages
import userDAO

def save_submission(username, submission, exercise_id, verdict):
    user_id = userDAO.get_user_id(username)
    sql = "INSERT INTO submissions (user_id, submission, exercise_id, date, verdict) VALUES (:user_id, :submission, :exercise_id, NOW() AT TIME ZONE 'EET', :verdict)"
    db.session.execute(sql, {"user_id":user_id, "submission":submission, "exercise_id":exercise_id, "verdict":verdict})
    db.session.commit()
    
def get_submissions_by_user_id_and_exercise_id(username, exercise_id):
    user_id = userDAO.get_user_id(username)
    sql = "SELECT S.submission, S.date, S.verdict, U.username FROM submissions S, users U WHERE S.user_id=:user_id AND S.exercise_id=:exercise_id AND U.id=:user_id ORDER BY date DESC"
    result = db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id})
    return result.fetchall()

def get_submissions_by_exercise_id(exercise_id):
    sql = "SELECT S.submission, S.date, S.verdict, U.username FROM submissions S, users U WHERE S.exercise_id=:exercise_id AND U.id=S.user_id ORDER BY date DESC"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()

def is_exercise_solved(username, exercise_id):
    user_id = userDAO.get_user_id(username)
    sql = "SELECT COUNT(*) FROM submissions WHERE user_id=:user_id AND exercise_id=:exercise_id AND verdict = 'OK'"
    result = db.session.execute(sql, {"user_id":user_id, "exercise_id":exercise_id})
    solved_cnt = result.fetchone()[0]
    if solved_cnt > 0:
        return True
    return False

def get_successful_submissions_count(exercise_id):
    sql = "SELECT COUNT(DISTINCT user_id) FROM submissions WHERE exercise_id=:exercise_id AND verdict = 'OK'"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    cnt = result.fetchone()[0]
    return cnt

def get_all_submissions_count(exercise_id):
    sql = "SELECT COUNT(DISTINCT user_id) FROM submissions WHERE exercise_id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    cnt = result.fetchone()[0]
    return cnt

def get_newest_submission_time(exercise_id):
    sql = "SELECT date FROM submissions WHERE exercise_id=:exercise_id ORDER BY date DESC"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    ans = result.fetchone()
    if ans == None:
        return None
    newest = result.fetchone()[0]
    return newest

def post_comment(username, comment, exercise_id):
    sql = "INSERT INTO comments (comment, username, exercise_id, date) VALUES (:comment, :username, :exercise_id, NOW() AT TIME ZONE 'EET')"
    db.session.execute(sql, {"comment":comment, "username":username, "exercise_id":exercise_id})
    db.session.commit()

def get_comments(exercise_id):
    sql = "SELECT comment, username, date FROM comments WHERE exercise_id=:exercise_id ORDER BY date DESC"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()

def get_leaderboard():
    sql = "SELECT U.username, COUNT(DISTINCT S.exercise_id) result FROM users U, submissions S WHERE U.id=S.user_id AND S.verdict = 'OK' GROUP BY U.id ORDER BY result DESC;"
    result = db.session.execute(sql)
    return result.fetchall()
