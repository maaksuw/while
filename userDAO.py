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
    
def invalidUsername(username):
    if len(username) < 3: return True
    return False

def invalidPassword(password):
    if len(password) < 8: return True
    regex = re.compile("([a-zA-Z]|[öäå]|[ÖÄÅ])*[0-9]([a-zA-Z]|[öäå]|[ÖÄÅ]|[0-9])*")
    if regex.fullmatch(password) == None: return True
    return False
