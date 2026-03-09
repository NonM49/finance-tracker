from flask import (Blueprint, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3

dash = Blueprint("dash", __name__)

@dash.route("/")
@dash.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        flash("Login first!", category="error")
        return redirect(url_for("auth.login"))
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT amount, type, description FROM transactions WHERE user_id=?",(session["user_id"],)
    )
    
    transactions = cur.fetchall()

    balance = 0
    for t in transactions:
        if t[1] == "income":
            balance += t[0]
        else:
            balance -= t[0]

    conn.close()

    return render_template("dashboard.html", transactions=transactions, balance=balance)