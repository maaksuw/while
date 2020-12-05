from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import messages

def get_password(username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def create_user(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE) RETURNING id"
        result = db.session.execute(sql, {"username":username, "password":hash_value})
        user_id = result.fetchone()[0]
        sql = "INSERT INTO profiles (user_id, introduction, joined) VALUES (:user_id, ' ', NOW())"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        return True
    except:
        return False
    
def existing_user(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    if result.fetchone() == None:
        return False
    return True
    
def get_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def invalidUsername(username):
    if len(username) < 3 or len(username) > 100: return True
    regex = messages.valid_username()
    if regex.fullmatch(username): return False
    return True

def invalidPassword(password):
    if len(password) < 8 or len(password) > 100: return True
    regex = messages.valid_password()
    if regex.fullmatch(password): return False
    return True

def is_admin(username):
    sql = "SELECT admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    admin = result.fetchone() 
    if admin == None:
        return False
    return admin[0]

def get_profile(username):
    user_id = get_user_id(username)
    sql = "SELECT introduction, joined FROM profiles WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def update_introduction(username, introduction):
    user_id = get_user_id(username)
    sql = "UPDATE profiles SET introduction=:introduction WHERE user_id=:user_id"
    db.session.execute(sql, {"introduction":introduction, "user_id":user_id})
    db.session.commit()
