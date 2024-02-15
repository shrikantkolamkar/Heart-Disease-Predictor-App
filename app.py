from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Replace with your MongoDB connection details
app.config["MONGO_URI"] = "mongodb://localhost:27017/HospitalManagement"
mongo = PyMongo(app)

# Define a collection for storing user data
users = mongo.db.users
Patients = mongo.db.Patients
Doctors  = mongo.db.Doctors
Appointments = mongo.db.Appointments


@app.route("/")
def home():
    return render_template("index.html")

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

@app.route("/dashboard.html")
def dashboard():
    # fetch details from database
    patients = Patients.find().sort('date_time', -1)

    # Fetch counts from MongoDB collections

    doctors_count = Doctors.count_documents({})
    patients_count = Patients.count_documents({})
    schedules_count = Appointments.count_documents({})
    beds_available = Appointments.count_documents({})

    # Pass data to the HTML template
    return render_template('dashboard.html',
                           doctors_count=doctors_count,
                           patients_count=patients_count,
                           schedules_count=schedules_count,
                           beds_available=beds_available,
                           patients=patients)


@app.route("/schedule.html", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        # Handle form submission
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        department = request.form["department"]
        date_time = request.form["date_time"]
        reason = request.form["reason"]

        # Insert data into MongoDB using Patients collection
        patient_data = {
            "name": name,
            "age": age,
            "gender":gender,
            "email": email,
            "phone": phone,
            "address": address,
            "department": department,
            "date_time": date_time,
            "reason": reason
        }
        Patients.insert_one(patient_data)

        # Fetch the inserted document from MongoDB for review
        inserted_patient = Patients.find_one({"name": name, "email": email, "phone": phone})

        # Render the review template with the inserted patient details
        return render_template("review.html", patient=inserted_patient)

    # If it's a GET request, render the schedule form
    return render_template("schedule.html")

@app.route('/patients.html', methods=['GET'])
def patients():
    # Fetch all records from the 'patients' collection
    records = list(mongo.db.Patients.find())
    # Pass the records to the template
    return render_template('patients.html', records=records)

# Search by name route
@app.route('/search', methods=['GET'])
def search_by_name():
    name = request.args.get('name')
    records = mongo.db.patients.find({"name": {"$regex": name, "$options": "i"}})
    return render_template('patients_table.html', records=records)

# Update by name route
@app.route('/update', methods=['POST'])
def update_by_name():
    name = request.form["name"]
    updated_data = {
        "email": request.form["email"],
        "phone": request.form["phone"],
        "address": request.form["address"],
        "department": request.form["department"],
        "date_time": request.form["date_time"],
        "reason": request.form["reason"]
    }
    mongo.db.patients.update_many({"name": name}, {"$set": updated_data})
    return jsonify({"message": "Records updated successfully"})

# Delete by name route
@app.route('/delete', methods=['POST'])
def delete_by_name():
    name = request.form["name"]
    mongo.db.patients.delete_many({"name": name})
    return jsonify({"message": "Records deleted successfully"})

@app.route('/heart_stroke_predictor.html', methods = ['GET', 'POST'])
def heart_stroke_prediction():
    return render_template('heart_stroke_predictor.html')

@app.route('/doctors.html', methods=['GET', 'POST'])
def doctors():
    Doctors = mongo.db.Doctors
    if request.method == 'POST':
        # Your existing code to collect form data and insert into the database
        Doctors.insert_one({
            "name": request.form['name'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "address": request.form['address'],
            "specialization": request.form['specialization'],
            "previous_hospital": request.form['previous_hospital'],
            "years_of_exp": request.form['experience']
        })
        # Redirect to the dashboard after successful submission
        return redirect(url_for('dashboard'))
    # Your code continues for a GET request
    return render_template('doctors.html')

@app.route('/index.html')
def logout():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)