from flask import Blueprint

main = Blueprint('main', __name__)

# from main import routes  # import routes after blueprint
from . import routes