from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates', static_folder='static')

from aat.errors import routes
