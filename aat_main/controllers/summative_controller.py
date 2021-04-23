import json
import datetime
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from jinja2 import TemplateError

from flask_login import current_user

from aat_main.forms.summative_forms import assessment_form, summative_edit_form
from aat_main.models.assessment_models import Assessment
from aat_main.models.question_models import Question
from aat_main.models.enrolment_models import ModuleEnrolment
from aat_main.utils.api_exception_helper import NotFoundException
from aat_main.models.module_model import Module
from aat_main import db

summative_blueprint = Blueprint('summative_blueprint', __name__, template_folder='../views/summative')

@summative_blueprint.route('/assessments/assessments_management/summative/', methods=['GET', 'POST'])
def summative():
    questions = Question.get_all()
    form = assessment_form()
    module_db = Module.get_all()
 
    module_choices = [(mod.code, (f'{mod.code}  :  {mod.name}')
        ) for mod in db.session.query(
        Module).join(ModuleEnrolment,Module.code == ModuleEnrolment.module_code
        ).filter(ModuleEnrolment.account_id == current_user.id).all()]
    module_choices.insert(0,("Please Choose a Module", "Please Choose a Module"))
    form.module.choices = module_choices

    if request.method == "POST":
        if form.validate_on_submit():
            added_questions = []
            # Checks if checkbox is active. If yes, adds value to added questions.
            for question in questions:
                question_id = request.form.get(str(question.id))
                if question_id:
                    added_questions.append(question_id)

            module_code = form.module.data.split()
            module_code = module_code[0]

            # Convert Datetime's
            start_datetime = Assessment.convert_datetime(form.start_date.data, form.start_time.data)
            end_datetime = Assessment.convert_datetime(form.end_date.data, form.end_time.data)

            added_questions = json.dumps(added_questions)
            type = 1
            count_in = 0
            attempts = 1
            Assessment.create_assessment(form.title.data, added_questions, form.description.data, module_code, type, count_in, attempts,
                                         start_datetime, end_datetime, form.timelimit.data, datetime.now())
            return redirect(url_for('assessment_bp.assessments'))

    return render_template("summative.html", form=form, questions=questions, modules=module_choices)
    # try:
    #     return render_template('summative.html')
    # except TemplateError:
    #     raise NotFoundException()

@summative_blueprint.route('/assessments/assessment_management/<int:assessment_id>')
def summative_edit(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = summative_edit_form()
    questions = Question.get_all()

    added_questions = assessment.questions

    availdate = assessment.availability_date
    startdate = availdate.date()
    starttime = availdate.strftime("%H:%M:%S")

    duedate = assessment.due_date
    enddate = duedate.date()
    endtime = duedate.strftime("%H:%M:%S")

    if request.method == "POST":
        if form.validate_on_submit():
            added_questions = []
            # Checks if checkbox is active. If yes, adds value to added questions.
            for question in questions:
                question_id = request.form.get(str(question.id))
                if question_id:
                    added_questions.append(question_id)

            added_questions = json.dumps(added_questions)

            # Convert Datetime's
            
            start_datetime = Assessment.convert_datetime(start_date = request.form.get("start_date"), start_time = request.form.get("start_time"))
            end_datetime = Assessment.convert_datetime(end_date = request.form.get("end_date"), end_time = request.form.get("end_time") )

            title = request.form.get("title_form")

            timelimit = request.form.get("timelimit_form")

            description = request.form.get("description_form")

            assessment_id = assessment.id

            type = 1
            count_in = 0
            attempts = 1
            Assessment.update_assessment(title, added_questions, description, module_code, type, count_in, attempts,
                                         start_datetime, end_datetime, timelimit, datetime.now(), asssessment_id)
            return redirect(url_for('assessment_bp.assessments'))
    
    return render_template("summative_edit.html", assessment=assessment, form=form, 
    questions=questions, startdate=startdate, starttime=starttime, 
    enddate=enddate, endtime=endtime, added_questions=added_questions)

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
#     return render_template('error.html', api_exception=api_exception
