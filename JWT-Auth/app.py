from flask import Flask
from auth import auth_bp
from profile import profile_bp
from db import init_db

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    init_db()  # Create table if not exists
    app.run(debug=True)
