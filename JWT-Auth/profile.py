from flask import Blueprint, request, jsonify
import jwt
from functools import wraps
from db import get_db_connection

SECRET_KEY = 'your_secret_key'

profile_bp = Blueprint('profile', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 403

        return f(user_id, *args, **kwargs)

    return decorated

@profile_bp.route('/profile', methods=['GET'])
@token_required
def profile(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT id, username FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    return jsonify({'id': user['id'], 'username': user['username']})
