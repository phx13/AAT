from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.utils.api_exception_helper import NotFoundException

question_blueprint = Blueprint('question_blueprint', __name__)


@question_blueprint.route('/')
def index_page():
    try:
        return render_template('index.html')
    except TemplateError:
        raise NotFoundException()
