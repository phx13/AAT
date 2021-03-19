from flask import Blueprint, render_template
from jinja2 import TemplateError

from aat_main.utils.api_exception_helper import NotFoundException

course_blueprint = Blueprint('course_blueprint', __name__)


@course_blueprint.route('/course/')
def course_page():
    try:
        return render_template('course.html')
    except TemplateError:
        raise NotFoundException()


@course_blueprint.route('/course/assessment/')
def course_assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()