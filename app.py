from flask import (Flask, render_template, request,
                    flash, redirect, session, url_for)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth import auth
from routes.finance import fina
from routes.dashboard import dash
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth)
app.register_blueprint(fina)
app.register_blueprint(dash)

if __name__ == "__main__":
    app.run(debug=True)