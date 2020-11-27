from flask import Flask
from db import db
import messages

def get_exercise(id):
    sql = "SELECT heading, description, topic, input_size FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    exercise = result.fetchone()
    return exercise

def get_exercises_by_topic_order_by_heading(topic):
    sql = "SELECT id, heading FROM exercises WHERE topic=:topic ORDER BY heading"
    result = db.session.execute(sql, {"topic":topic})
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
    
def update_exercise(heading, description, topic, input_size, id):
    sql = "UPDATE exercises SET heading=:heading, description=:description, topic=:topic, input_size=:input_size WHERE id=:id"
    db.session.execute(sql, {"heading":heading, "description":description, "topic":topic, "input_size":input_size, "id":id})
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
