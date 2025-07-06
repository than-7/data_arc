import bcrypt

# Mock user database
users = [
    {
        'id': 1,
        'username': 'admin',
        # Password is "password123" hashed
        'password': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'email': 'admin@example.com',
        'role': 'admin'
    }
]