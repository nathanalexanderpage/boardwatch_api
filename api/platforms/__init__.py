from flask import Blueprint

bp = Blueprint('platforms', __name__)

from api import routes
