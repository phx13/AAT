from flask import Blueprint, render_template, redirect, url_for
from jinja2 import TemplateError

from aat_main.forms.question_form import question_form
from aat_main.models.question_models import Question
from aat_main.utils.api_exception_helper import NotFoundException

question_blueprint = Blueprint('question_blueprint', __name__, template_folder='../views')


@question_blueprint.route('/questions/', methods=['GET', 'POST'])
def questions():
    form = question_form()
    if form.validate_on_submit():
        Question.create_question(form.name.data, form.description.data, form.course.data)
        return redirect(url_for('course_bp.assessments'))

    return render_template("create_question.html", form=form)
    # try:
    #     return render_template('question.html')
    # except TemplateError:
    #     raise NotFoundException()
