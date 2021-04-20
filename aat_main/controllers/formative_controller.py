import json
from flask import Blueprint, render_template, redirect, url_for, request, flash
from jinja2 import TemplateError

from aat_main.forms.formative_forms import module_choice_form
from aat_main.models.assessment_models import Assessment
from aat_main.utils.api_exception_helper import NotFoundException
from aat_main.models.module_model import Module

formative_blueprint = Blueprint('formative_blueprint', __name__, template_folder='../views/formative')


@formative_blueprint.route('/assessments/assessments_management/formative/', methods=['GET', 'POST'])
def formative():
    form = module_choice_form()
    message = 'Nothing Now'
    if request.method == "POST":
        if form.validate_on_submit():
            # Gets module code
            module_code = form.module.data[:6]
            message = module_code

            return message

    return render_template("formative.html", form=form, message=message)


@formative_blueprint.route('/course/assessment/')
def course_assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()

# @formative_blueprint.errorhandler(404)
# def catch_http_exception(e):
#     if isinstance(e, HTTPException):
#         api_exception = APIException(e.code, e.description)
#     else:
#         api_exception = InterServerErrorException()
#     return render_template('error.html', api_exception=api_exception)
