from db import db

def get_destinations():
    sql = "SELECT id, address, phone_number, description FROM destinations"
    result = db.session.execute(sql)
    return result.fetchall()

def get_destination_info(destination_id):
    sql = "SELECT id, address, phone_number, description FROM destinations WHERE id=:destination_id"
    return db.session.execute(sql, {"destination_id": destination_id}).fetchone()