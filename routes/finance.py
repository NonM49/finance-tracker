from flask import (Blueprint, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3

fina = Blueprint("fina", __name__)

@fina.route("/add", methods=["GET","POST"])
def add():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        amount = request.form["amount"]
        type = request.form["type"]
        description = request.form["description"]

        # validation
        if not amount:
            return flash("Amount required", category="error")

        try:
            amount = float(amount)
        except ValueError:
            return flash("Amount must be a number", category="error")

        if type not in ["income", "expense"]:
            return flash("Invalid type", category="error")
        
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO transactions (user_id, amount, type, description) VALUES (?, ?, ?, ?)",
            (session["user_id"], amount, type, description)
        )

        conn.commit()
        conn.close()

        flash("Added!", category="success")

        return redirect(url_for("dash.dashboard"))

    return render_template("add.html")