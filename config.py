import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'charandetect')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
