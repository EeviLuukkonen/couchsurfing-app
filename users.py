from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        session["user_id"] = user[0]
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return True
        else:
            return False

def get_user_info(user_id):
    sql = "SELECT u.username, d.id, d.address FROM users u, destinations d WHERE user_id=:user_id AND d.user_id=u.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def user_id():
    return session.get("user_id")

def logout():
    del session["username"]
