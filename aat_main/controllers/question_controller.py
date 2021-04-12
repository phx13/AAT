from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from jinja2 import TemplateError

from aat_main import db
from aat_main.models.question_models import Question
from aat_main.utils.api_exception_helper import NotFoundException

# TODO this has the same name as the blueprint in create_question_controller. fix this
question_bp = Blueprint('question_bp', __name__, template_folder='../views/question', url_prefix='/questions')


@question_bp.route('/course/assessment/<int:assessment_id>')
def assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>')
def type_one_question_page():
    try:
        return render_template('type_one_question.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>')
def type_two_question_page():
    try:
        return render_template('type_two_question.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/edit')
def edit_type_one_question_edit_page():
    try:
        return render_template('type_one_question_edit.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/edit')
def edit_type_two_question_edit_page():
    try:
        return render_template('type_two_question_edit.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/save')
def edit_type_one_question():
    try:
        return render_template('type_one_question.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/save')
def save_type_two_question():
    try:
        return render_template('type_two_question.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
def edit_type_one_question_remove():
    try:
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/completed/')
def completed_questions():
    questions = current_user.get_completed_questions()
    return render_template('completed_questions.html', questions=questions)


@question_bp.route('/manage')
def manage_questions():
    # TODO this is just to test functionality. implement it properly
    questions = db.session.query(Question).all()
    return render_template('question_management.html', questions=questions)
