from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import re

def getPassword(username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def createNewUser(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def getExercise(id):
    sql = "SELECT heading, description, topic FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    exercise = result.fetchone()
    return (exercise[0], exercise[1], exercise[2])

def getExercisesByTopic(topic):
    sql = "SELECT id, heading FROM exercises WHERE topic=:topic"
    result = db.session.execute(sql, {"topic":topic})
    return result.fetchall()

def createNewExercise(heading, description, topic):
    sql = "INSERT INTO exercises (heading, description, topic) VALUES (:heading, :description, :topic) RETURNING id"
    result = db.session.execute(sql, {"heading":heading, "description":description, "topic":topic})
    exercise_id = result.fetchone()[0]
    db.session.commit()
    return exercise_id

def createNewTest(exercise_id, input, output):
    sql = "INSERT INTO tests (exercise_id, input, output) VALUES (:exercise_id, :input, :output)"
    db.session.execute(sql, {"exercise_id":exercise_id, "input":input, "output":output})
    db.session.commit()
    
def getTests(exercise_id):
    sql = "SELECT input, output FROM tests WHERE exercise_id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()

def update_exercise(heading, description, topic, id):
    sql = "UPDATE exercises SET heading=:heading, description=:description, topic=:topic WHERE id=:id"
    db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "id":id})
    db.session.commit()

def invalidUsername(username):
    if len(username) < 3: return True
    return False

def invalidPassword(password):
    if len(password) < 8: return True
    regex = re.compile("([a-zA-Z]|[öäå]|[ÖÄÅ])*[0-9]([a-zA-Z]|[öäå]|[ÖÄÅ]|[0-9])*")
    if regex.fullmatch(password) == None: return True
    return False
