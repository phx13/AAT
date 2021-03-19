from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.models.account_model import AccountModel
from aat_main.utils.api_exception_helper import NotFoundException

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')


@auth_blueprint.route('/login')
def login():
    try:
        return render_template('login.html')
    except TemplateError:
        raise NotFoundException()
