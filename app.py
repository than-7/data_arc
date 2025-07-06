from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 🔐 Use strong key in production

# Dummy user for demonstration
USER_DATA = {
    "username": "admin",
    "password": "1234"
}

# Middleware to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# 📥 Login Route
@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Missing credentials!'}), 400

    if auth['username'] != USER_DATA['username'] or auth['password'] != USER_DATA['password']:
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Create token valid for 30 minutes
    token = jwt.encode({
        'user': auth['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# 👤 Protected Profile Route
@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({'message': f'Welcome {current_user}, this is your profile.'})

# 🔃 Test route (public)
@app.route('/')
def home():
    return "Welcome to the JWT Auth API!"

if __name__ == '__main__':
    app.run(debug=True)
