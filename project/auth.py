from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from models import users

login_bp = Blueprint('login', __name__)
profile_bp = Blueprint('profile', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Find user in database
    user = next((u for u in users if u['username'] == username), None)
    
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"msg": "Bad username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)
    
    return jsonify(access_token=access_token), 200

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    
    # Find user in database
    user = next((u for u in users if u['username'] == current_user), None)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Return user data without password
    user_data = {k: v for k, v in user.items() if k != 'password'}
    return jsonify(user_data), 200