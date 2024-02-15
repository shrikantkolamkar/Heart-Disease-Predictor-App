from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from HealthSage.models import authenticate_user  # Update import
# Creates a Blueprint for authentication
auth = Blueprint('auth', __name__)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user data from MongoDB
        user_data = users.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            return redirect(url_for("dashboard"))

        print("The credentials are Invalid")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Basic validation
        if not email or not username or not password:
            return render_template("signup.html", error="Please fill in all fields.")

        # Check if username or email already exists
        existing_user = users.find_one({"$or": [{"email": email}, {"username": username}]})
        if existing_user:
            return render_template("signup.html", error="Username or email already exists.")

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Insert user data into MongoDB
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        users.insert_one(user_data)

        # Redirect to the login page after successful signup
        return redirect(url_for("login"))

    return render_template("signup.html")