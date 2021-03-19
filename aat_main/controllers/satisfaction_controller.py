from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.models.account_model import AccountModel
from aat_main.utils.api_exception_helper import NotFoundException

satisfaction_blueprint = Blueprint('satisfaction_blueprint', __name__, url_prefix='/review', template_folder='views/satisfaction')


@satisfaction_blueprint.route('/assessment/<id>')
def assessment_review(id):
    print(id)
    try:
        return render_template('assessment_review.html', assessment_id=id)
    except TemplateError:
        raise NotFoundException()
