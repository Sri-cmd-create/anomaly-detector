from datetime import datetime
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    success = db.Column(db.Boolean, nullable=False)
    ip_address = db.Column(db.String(100))
    user_agent = db.Column(db.String(300))
    location = db.Column(db.String(300))
    
    # CREATE TABLE login_attempt (
    #     id INTEGER NOT NULL, 
    #     username VARCHAR(80) NOT NULL, 
    #     ip_address VARCHAR(45) NOT NULL, 
    #     timestamp DATETIME NOT NULL, 
    #     PRIMARY KEY (id)
    # )