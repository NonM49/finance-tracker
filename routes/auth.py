from flask import (Blueprint, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # validation
        if not username or not password:
            flash("Username and password required")
            return render_template("register.html")
        
        hashed_password = generate_password_hash(password)
        
        if len(password) < 6:
            flash("Password must be at least 6 characters")
            return render_template("register.html")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # check if user exists
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            flash("Username already exists")
            return render_template("register.html")

        cur.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, hashed_password)
)
        conn.commit()
        conn.close()
        flash("User registered!")

        return redirect("/")

    return render_template("register.html")

@auth.route("/")
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            username = session.get("username")
            
            flash(f"Login successful!, {username}")
            return redirect(url_for("dash.dashboard"))
        
        flash("Invalid username or password")
        return render_template("login.html")
    
    return render_template("login.html")

@auth.route("/logout")
def logout():
    username = session.get("username")
    session.pop("username", None)

    flash(f"Logged out successful!, {username} ")
    return redirect(url_for("auth.login"))