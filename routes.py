from os import error
from flask import render_template, request, redirect
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
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if 3 > len(username) > 20:
            return render_template("error.html", error="Käyttäjänimen pituuden tulee olla 3-20 merkkiä")

        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")

        if 3 > len(password1) > 20:
            return render_template("error.html", message="Salasanan pituuden tulee olla 3-20 merkkiä")

        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error=True)

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
            return render_template("error.html", message="Kommentti on liian pitkä")
        if description == "" or address == "" or phone_number == "":
            return render_template("/new.html", error=True)

        user = users.user_id()
        print(user)
        if user:
            if destinations.new_destination(user, address, phone_number, description):
                return render_template("/new.html", success=True)   
        else:
            return render_template("/new.html", error=True)         

@app.route("/destination/<int:destination_id>")
def show_destination(destination_id):
    info = destinations.get_destination_info(destination_id)
    reviews = destinations.get_reviews(destination_id)
    return render_template("destination.html", id=destination_id, user=info[0], address=info[1], phone_number=info[2], description=info[3], reviews=reviews)

@app.route("/review", methods=["post"])
def review():
    destination_id = request.form["destination_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("destination.html", error=True, message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 500:
        return render_template("destination.html", error=True, message="Liian pitkä kommentti!")
    if comment == "":
        comment = "-"

    destinations.add_review(users.user_id(), destination_id, stars, comment)

    return redirect("/destination/"+str(destination_id))