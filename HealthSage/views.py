from flask import Blueprint, render_template, request, redirect, url_for
from . import PyMongo  # This needs to be adjusted based on how you initialize PyMongo

main = Blueprint('main', __name__)

@app.route("/")
def home():
    return render_template("index.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use the authenticate_user function from models.py
        if authenticate_user(username, password):
            return redirect(url_for("dashboard"))
        else:
            # If authentication fails
            error = "Invalid credentials"
            return render_template("login.html", error=error)

    # For GET requests, or if POST but not authenticated
    return render_template("login.html")

