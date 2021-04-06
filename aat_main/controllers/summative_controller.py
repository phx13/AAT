from flask import Blueprint, render_template, redirect, url_for
from jinja2 import TemplateError

from aat_main.forms.summative_forms import assessment_form
from aat_main.models.assessment_models import Assessment
from aat_main.utils.api_exception_helper import NotFoundException

summative_blueprint = Blueprint('summative_blueprint', __name__, template_folder='../views/summative')


@summative_blueprint.route('/assessments/assessments_management/summative/', methods=['GET', 'POST'])
def summative():
    form = assessment_form()
    if form.validate_on_submit():
        Assessment.create_assessment(form.title.data)
        return redirect(url_for('course_bp.assessments'))

    return render_template("summative.html", form=form)
    # try:
    #     return render_template('summative.html')
    # except TemplateError:
    #     raise NotFoundException()


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
