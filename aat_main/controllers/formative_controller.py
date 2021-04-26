from flask import Blueprint, render_template, request, jsonify
from jinja2 import TemplateError
from datetime import datetime

from aat_main.forms.formative_forms import module_choice_form
from aat_main.models.assessment_models import Assessment
from aat_main.utils.api_exception_helper import NotFoundException
from aat_main.utils.serialization_helper import SerializationHelper

formative_blueprint = Blueprint('formative_blueprint', __name__, template_folder='../views/formative')


@formative_blueprint.route('/assessments/assessments_management/formative/', methods=['GET', 'POST'])
def formative():
    form = module_choice_form()
    message = 'Nothing Now'
    if request.method == "POST":
        if form.validate_on_submit():
            # Gets module code
            module_code = form.module.data.split(':')[0]
            message = module_code

            return message

    return render_template("formative.html", form=form, message=message)


@formative_blueprint.route('/assessments/assessments_management/formative/<string:status>/<string:module>')
def assessment_data(status, module):
    try:
        current_time = datetime.now()
        if status == 'current':
            if module == 'Please Choose a Module':
                origin_data = Assessment.get_all_current(current_time)
            else:
                origin_data = Assessment.get_all_current_by_module(module, current_time)
        else:
            if module == 'Please Choose a Module':
                origin_data = Assessment.get_all_pass(current_time)
            else:
                origin_data = Assessment.get_all_pass_by_module(module, current_time)

        data = []
        for od in origin_data:
            dic = {
                'id': od.id,
                'title': od.title,
                'release_time': od.availability_date,
                'deadline': od.due_date
            }
            data.append(dic)
        if request.method == 'GET':
            info = request.values
            limit = info.get('limit', 10)
            offset = info.get('offset', 0)
        return jsonify({
            'total': len(data),
            'rows': data[int(offset):(int(offset) + int(limit))]
        })
    except:
        return 'server error'


@formative_blueprint.route('/assessments/assessments_management/formative/create/', methods=['POST'])
def create_assessment_data():
    try:
        # Assessment.create_assessment(1, 1, 1, 1, 1, 1, 1, datetime.now(), datetime.now(), 1)
        assessment = {}
        for k, v in request.form.items():
            assessment[k] = v
            print(k,'\t',v)
        formativeTitle = assessment['formativeTitle']
        releaseTime = datetime.fromisoformat(assessment['releaseTime'])
        dueDate = datetime.fromisoformat(assessment['dueDate'])
        countIn = int(assessment['countIn'])
        attemptTime = int(assessment['attemptTime'])
        timeLimit = int(assessment['timeLimit'])
        description = assessment['description']
        module = assessment['module']

        Assessment.create_assessment(formativeTitle, '', description, module, 0, countIn, attemptTime, releaseTime,
                                     dueDate, timeLimit, datetime.now())
        # Assessment.create_assessment(formativeTitle, '', description, module, 0, countIn, attemptTime, datetime.now(),
        #                              datetime.now(), timeLimit, datetime.now())
        return 'create successful'
    except:
        return 'Server error'


@formative_blueprint.route('/assessments/assessments_management/formative/delete/', methods=['POST'])
def delete_assessment_data():
    try:
        for k, v in request.form.items():
            Assessment.delete_assessment_by_id(k)
        return 'delete successful'
    except:
        return 'Server error'


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
