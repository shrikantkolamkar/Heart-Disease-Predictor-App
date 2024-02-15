from HealthSage import PyMongo
users = mongo.db.users
# from HealthSage.auth import login  # Update this import statement if necessary

from werkzeug.security import check_password_hash

def authenticate_user(username, password):
    """
    Authenticate a user by their username and password.
    Returns the user data if authentication is successful, None otherwise.
    """
    users = mongo.db.users
    user_data = users.find_one({"username": username})
    if user_data and check_password_hash(user_data["password"], password):
        return user_data
    return None
