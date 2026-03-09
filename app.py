from flask import (Flask, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth import auth
from routes.finance import fina
from routes.dashboard import dash

app = Flask(__name__)
app.secret_key = "Non53133"

app.register_blueprint(auth)
app.register_blueprint(fina)
app.register_blueprint(dash)

if __name__ == "__main__":
    app.run(debug=True)