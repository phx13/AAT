from flask import Blueprint, render_template
from jinja2 import TemplateError
from aat_main.utils.api_exception_helper import NotFoundException

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index_page():
    try:
        return render_template('index.html')
    except TemplateError:
        raise NotFoundException()
