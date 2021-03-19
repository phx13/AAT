from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.utils.api_exception_helper import NotFoundException

summative_blueprint = Blueprint('summative_blueprint', __name__, template_folder='../views/summative')


@summative_blueprint.route('/summative/')
def course_page():
    try:
        return render_template('summative.html')
    except TemplateError:
        raise NotFoundException()


@summative_blueprint.route('/course/assessment/')
def course_assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()


# @summative_blueprint.errorhandler(404)
# def catch_http_exception(e):
#     if isinstance(e, HTTPException):
#         api_exception = APIException(e.code, e.description)
#     else:
#         api_exception = InterServerErrorException()
#     return render_template('error.html', api_exception=api_exception)