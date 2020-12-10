from flask import Flask
from db import db
import messages
import userDAO

def get_exercise(id):
    sql = "SELECT heading, description, topic, input_size, exercise_order FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    exercise = result.fetchone()
    return exercise

def get_exercises_by_topic_in_order(topic, username):
    if username == None:
        sql = "SELECT id, heading, FALSE FROM exercises WHERE topic=:topic ORDER BY exercise_order"
        result = db.session.execute(sql, {"topic":topic})
    else:
        user_id = userDAO.get_user_id(username)
        sql = "SELECT id, heading, CASE WHEN id IN(SELECT DISTINCT exercise_id FROM submissions WHERE user_id=:user_id AND verdict='OK') THEN TRUE ELSE FALSE END FROM exercises WHERE topic=:topic ORDER BY exercise_order"
        result = db.session.execute(sql, {"topic":topic, "user_id":user_id})
    return result.fetchall()

def get_heading(id):
    sql = "SELECT heading FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def create_exercise(heading, description, topic, input_size):
    sql = "INSERT INTO exercises (heading, description, topic, input_size) VALUES (:heading, :description, :topic, :input_size) RETURNING id"
    result = db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "input_size":input_size})
    exercise_id = result.fetchone()[0]
    db.session.commit()
    return exercise_id
    
def update_exercise(heading, description, topic, input_size, exercise_order, id):
    sql = "UPDATE exercises SET heading=:heading, description=:description, topic=:topic, input_size=:input_size, exercise_order=:exercise_order WHERE id=:id"
    db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "input_size":input_size, "exercise_order":exercise_order, "id":id})
    db.session.commit()

def get_input_size(id):
    sql = "SELECT input_size FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
    
def create_test(exercise_id, input, output):
    sql = "INSERT INTO tests (exercise_id, input, output) VALUES (:exercise_id, :input, :output)"
    db.session.execute(sql, {"exercise_id":exercise_id, "input":input, "output":output})
    db.session.commit()
    
def get_tests(exercise_id):
    sql = "SELECT input, output, id FROM tests WHERE exercise_id=:exercise_id ORDER BY id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()
    
def update_test(input, output, id):
    sql = "UPDATE tests SET input=:input, output=:output WHERE id=:id"
    db.session.execute(sql, {"input":input, "output":output, "id":id})
    db.session.commit()
    
def remove_test(id):
    sql = "DELETE FROM tests WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
