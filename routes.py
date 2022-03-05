from os import error
import re
from flask import render_template, request, redirect, sessions
from app import app
from db import db
import users
import destinations

@app.route("/")
def index():
    list = destinations.get_destinations()
    return render_template("index.html", destinations=list)

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error="Käyttäjätunnus ja salasana eivät täsmää!")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if 3 > len(username) > 20:
            return render_template("error.html", message="Käyttäjänimen pituuden tulee olla 3-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")

        if password1 == "":
            return render_template("error.html", message="Salasanan pituuden tulee olla 3-20 merkkiä")

        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Tunnuksen luonti epäonnistui!")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new", methods=["get", "post"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    
    if request.method == "POST":
        address = request.form["address"]
        phone_number = request.form["phone_number"]
        description = request.form["description"]

        if len(description) > 500:
            return render_template("/error.html", message="Kommentti on liian pitkä")
        if description == "" or address == "" or phone_number == "":
            return render_template("/error.html", message="Kohteen lisäys epäonnistui. Täytä kaikki kohdat!")
        
        if len(phone_number) != 10:
            return render_template("/error.html", message="Tarkista puhelinnumeron pituus (10 merkkiä)!")

        user = users.user_id()

        if user:
            if destinations.new_destination(user, address, phone_number, description):
                return render_template("/new.html", success=True)   
        else:
            return render_template("/new.html", error=True)         

@app.route("/destination/<int:destination_id>")
def show_destination(destination_id):
    info = destinations.get_destination_info(destination_id)
    reviews = destinations.get_reviews(destination_id)
    return render_template("destination.html", id=destination_id, user=info[0], address=info[1], phone_number=info[2], description=info[3], reviews=reviews, user_id=info[4])

@app.route("/review", methods=["post"])
def review():
    destination_id = request.form["destination_id"]
    user_id = request.form["user_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("destination.html", error=True, message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 500:
        return render_template("error.html", message="Kommentin tulee olla alle 500 merkkiä pitkä.")
    if comment == "":
        return render_template("error.html", message="Kommentti ei saa olla tyhjä!")
    
    if int(users.user_id()) == int(user_id):
        return render_template("error.html", message="Et voi arvioida omaa kohdettasi!")
    
    reviews = destinations.get_reviews(destination_id)
    for review in reviews:
        if review[0] == users.user_id():
            return render_template("error.html", message="Olet jo arvioinut tämän kohteen!")

    destinations.add_review(users.user_id(), destination_id, stars, comment)

    return redirect("/destination/"+str(destination_id))

@app.route("/user_review", methods=["post"])
def user_review():
    reviewer_id = request.form["reviewer_id"]
    user_id = request.form["user_id"]
    destination_id = request.form["destination_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("destination.html", error=True, message="Virheellinen tähtimäärä")
    
    comment = request.form["comment"]
    if len(comment) > 200:
        return render_template("error.html", message="Kommentin tulee olla alle 200 merkkiä pitkä.")
    if comment == "":
        return render_template("error.html", message="Kommentti ei saa olla tyhjä!")
    
    user_reviews = users.get_user_reviews(reviewer_id)
    for review in user_reviews:
        if review[0] == users.user_id():
            return render_template("error.html", message="Olet jo arvioinut tämän vierailijan!")

    users.add_user_review(reviewer_id, user_id, stars, comment)

    return redirect("/destination/"+str(destination_id))

@app.route("/user/<int:user_id>")
def show_user_info(user_id):
    username = users.get_user_info(user_id)
    list = users.get_users_destinations(user_id)
    visits = users.get_users_visits(user_id)
    
    comments = users.get_user_comments(user_id)
    score = users.get_user_score(user_id)

    if list == []:
        return render_template("user.html", username = username)
    else:
        return render_template("user.html", destinations=list, username=username, visits=visits, comments=comments, userscore=score)