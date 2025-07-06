from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'  # Use a strong secret key in real apps

# ----- Database Setup -----
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insert a test user if not exists
    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('john', '1234'))
    conn.commit()
    conn.close()

# ----- JWT Middleware -----
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(user_id, *args, **kwargs)
    return decorated

# ----- Login Route -----
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", 
                        (username, password)).fetchone()
    conn.close()

    if user:
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# ----- Protected Profile Route -----
@app.route('/profile', methods=['GET'])
@token_required
def profile(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, username FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()

    if user:
        return jsonify({'id': user['id'], 'username': user['username']})
    else:
        return jsonify({'message': 'User not found'}), 404

# ----- Run the App -----
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
