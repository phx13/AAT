from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.models.account_model import AccountModel
from aat_main.utils.api_exception_helper import NotFoundException

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    return render_template('login.html')
