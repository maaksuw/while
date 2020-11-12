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
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def getExercise(id):
    sql = "SELECT heading, description FROM exercises WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    exercise = result.fetchone()
    return (exercise[0], exercise[1])

def getExercisesByTopic(topic):
    sql = "SELECT id, heading FROM exercises WHERE topic=:topic"
    result = db.session.execute(sql, {"topic":topic})
    return result.fetchall()
