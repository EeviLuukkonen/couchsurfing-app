from flask import render_template, request, redirect
from app import app
from db import db
import users

@app.route("/")
def index():
    return render_template("index.html")

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
            return render_template("login.html", error=True)

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
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

        try:
            sql = "INSERT INTO destinations (address, phone_number, description) VALUES (:address, :phone_number, :description)"
            db.session.execute(sql, {"address":address, "phone_number":phone_number, "description":description})
            db.session.commit()
            return render_template("/new.html", success=True)            
        except:
            return render_template("/new.html", error=True)