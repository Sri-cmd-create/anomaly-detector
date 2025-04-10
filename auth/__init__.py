from flask import Blueprint

auth = Blueprint('auth', __name__)

# from auth import routes  # import routes after blueprint
from . import routes