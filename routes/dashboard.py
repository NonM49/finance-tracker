from flask import (Blueprint, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3

dash = Blueprint("dash", __name__)

@dash.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Login first!", category="error")
        return redirect(url_for("auth.login"))
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT id, amount, type, description FROM transactions WHERE user_id=?",(session["user_id"],)
    )
    
    transactions = cur.fetchall()

    balance = 0
    for t in transactions:
        if t[2] == "income":
            balance += t[1]
        else:
            balance -= t[1]

    cur.execute("""
    SELECT type, SUM(amount)
    FROM transactions
    WHERE user_id=?
    GROUP BY type
    """, (session["user_id"],))

    data = cur.fetchall()

    income = 0
    expense = 0

    for d in data:
        if d[0] == "income":
            income = d[1]
        else:
            expense = d[1]

    conn.close()

    return render_template("dashboard.html", transactions=transactions, balance=balance,
                           income=income, expense=expense)

@dash.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user_id" not in session:
        flash("Login first!", category="error")
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM transactions WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dash.dashboard"))
