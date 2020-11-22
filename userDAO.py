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
    sql = "SELECT heading, description, topic, input_size FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    exercise = result.fetchone()
    return exercise

def getExercisesByTopicOrderByHeading(topic):
    sql = "SELECT id, heading FROM exercises WHERE topic=:topic ORDER BY heading"
    result = db.session.execute(sql, {"topic":topic})
    return result.fetchall()

def createNewExercise(heading, description, topic, input_size):
    sql = "INSERT INTO exercises (heading, description, topic, input_size) VALUES (:heading, :description, :topic, :input_size) RETURNING id"
    result = db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "input_size":input_size})
    exercise_id = result.fetchone()[0]
    db.session.commit()
    return exercise_id
    
def update_exercise(heading, description, topic, input_size, id):
    sql = "UPDATE exercises SET heading=:heading, description=:description, topic=:topic, input_size=:input_size WHERE id=:id"
    db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "input_size":input_size, "id":id})
    db.session.commit()    
    
def createNewTest(exercise_id, input, output):
    sql = "INSERT INTO tests (exercise_id, input, output) VALUES (:exercise_id, :input, :output)"
    db.session.execute(sql, {"exercise_id":exercise_id, "input":input, "output":output})
    db.session.commit()
    
def getTests(exercise_id):
    sql = "SELECT input, output, id FROM tests WHERE exercise_id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()

def get_input_size(id):
    sql = "SELECT input_size FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
    
def update_test(input, output, id):
    sql = "UPDATE tests SET input=:input, output=:output WHERE id=:id"
    db.session.execute(sql, {"input":input, "output":output, "id":id})
    db.session.commit()
    
def remove_test(id):
    sql = "DELETE FROM tests WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def invalidUsername(username):
    if len(username) < 3: return True
    return False

def invalidPassword(password):
    if len(password) < 8: return True
    regex = re.compile("([a-zA-Z]|[öäå]|[ÖÄÅ])*[0-9]([a-zA-Z]|[öäå]|[ÖÄÅ]|[0-9])*")
    if regex.fullmatch(password) == None: return True
    return False
