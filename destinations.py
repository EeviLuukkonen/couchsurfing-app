from db import db

def get_destinations():
    sql = "SELECT d.id, d.address, COALESCE(CAST(AVG(r.stars) AS DECIMAL(10,2)),0) AS stars FROM destinations d LEFT JOIN reviews r ON r.destination_id=d.id GROUP BY d.id ORDER BY COALESCE(AVG(r.stars),0) DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_destination_info(destinationid):
    sql = "SELECT u.username, d.address, i.phone_number, i.description, u.id FROM info i, destinations d, users u WHERE d.id=:destinationid AND d.id=i.destination_id AND u.id=d.user_id"
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

def add_review(user_id, destination_id, stars, comment):
    sql = "INSERT INTO reviews (destination_id, user_id, stars, comment) VALUES (:destination_id, :user_id, :stars, :comment)"
    db.session.execute(sql, {"destination_id":destination_id, "user_id":user_id, "stars":stars, "comment":comment})
    db.session.commit()

def get_reviews(destination_id):
    sql = "SELECT u.id, u.username, r.stars, r.comment FROM reviews r, users u WHERE r.user_id=u.id AND r.destination_id=:destination_id ORDER BY r.id"
    return db.session.execute(sql, {"destination_id": destination_id}).fetchall()

def get_destination_stars(destination_id):
    sql = "SELECT AVG(stars) FROM destinations WHERE destination_id=:destination_id"
    return db.session.execute(sql, {"destination_id": destination_id}).fetchone[0]