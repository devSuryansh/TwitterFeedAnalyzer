import bcrypt
from db.mongo import get_user, insert_user

def signup_user(username, password):
    if get_user(username):
        return False, "Username already exists"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    insert_user(username, hashed)
    return True, "Signup successful"

def login_user(username, password):
    user = get_user(username)
    if not user:
        return False, "User not found"
    if bcrypt.checkpw(password.encode(), user['password']):
        return True, "Login successful"
    return False, "Incorrect password"
