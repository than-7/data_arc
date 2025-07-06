from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv
import os
from auth import login_bp, profile_bp

load_dotenv()

app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    app.run(debug=True)