from db import db

def get_destinations():
    sql = "SELECT id, address FROM destinations"
    result = db.session.execute(sql)
    return result.fetchall()

def get_destination_info(destinationid):
    sql = "SELECT d.address, i.phone_number, i.description FROM info i, destinations d WHERE d.id=:destinationid AND d.id=i.destination_id"
    return db.session.execute(sql, {"destinationid":destinationid}).fetchone()

def new_destination(user, address, phone_number, description):
    try:
        sql = "INSERT INTO destinations (user_id, address, visible) VALUES (:user, :address, 1) RETURNING id"
        destination_id = db.session.execute(sql, {"user":user, "address":address}).fetchone()[0]

        sql = "INSERT INTO info (destination_id, phone_number, description) VALUES (:destination_id, :phone_number, :description)"
        db.session.execute(sql, {"destination_id":destination_id, "phone_number":phone_number, "description":description})

        db.session.commit()
        return True
    except:
        return False
