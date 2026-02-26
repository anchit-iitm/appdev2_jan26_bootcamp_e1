from flask import Blueprint, request

from db import user_datastore, db
from security import ph

security_bp = Blueprint('security_apis', __name__)

@security_bp.route('/register', methods=['POST'])
def register():
    if not request.json:
        return {"message": "No data provided"}, 400
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    username = data.get('username')
    if not email or not password:
        return {"message": "Email and password are required"}, 400
    
    if "@" not in email:
        return {"message": "Invalid email"}, 400

    user = user_datastore.find_user(email=email)
    if user:
        return {"message": "User already exists"}, 400
    
    new_user = user_datastore.create_user(email=email, password=ph.hash(password))
    if username:
        new_user.username = username 
    if role == "manager":
        user_datastore.add_role_to_user(new_user, "manager")
        new_user.active = False
    else:
        user_datastore.add_role_to_user(new_user, "user")
    db.session.commit()
    return {"message": "User created successfully"}, 201
    
@security_bp.route('/login', methods=['POST'])
def login():
    if not request.json:
        return {"message": "No data provided"}, 400
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return {"message": "Email and password are required"}, 400
    user = user_datastore.find_user(email=email)
    if not user:
        return {"message": "User not found"}, 404
    if not ph.verify(user.password, password):
        return {"message": "Invalid password"}, 401
    if user.active:
        return {"message": "Login successful", "user": user.email, "token": user.get_auth_token()}, 200   
    return {"message": "User is not active"}, 400