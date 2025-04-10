import pickle

from flask import Flask, redirect, url_for
from extensions import db, migrate
from auth import auth  # fixed import
from config import Config
from flask_login import LoginManager
from models import User  # FIXED import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth)

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    # 🔥 Load AI models inside app
    with open('isolation_forest_model.pkl', 'rb') as f:
        isolation_model = pickle.load(f)

    with open('encoders.pkl', 'rb') as f:
        ip_encoder, browser_encoder, location_encoder = pickle.load(f)

    app.isolation_model = isolation_model
    app.ip_encoder = ip_encoder
    app.browser_encoder = browser_encoder
    app.location_encoder = location_encoder

    return app

