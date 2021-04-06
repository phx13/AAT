from flask import Blueprint, render_template, flash, request, redirect, url_for
from jinja2 import TemplateError

from aat_main.utils.api_exception_helper import NotFoundException

question_blueprint = Blueprint('question_blueprint', __name__)


@question_blueprint.route('/course/assessment/<int:assessment_id>')
def assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>')
def type_one_question_page():
    try:
        return render_template('type_one_question.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>')
def type_two_question_page():
    try:
        return render_template('type_two_question.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/edit')
def edit_type_one_question_edit_page():
    try:
        return render_template('type_one_question_edit.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/edit')
def edit_type_two_question_edit_page():
    try:
        return render_template('type_two_question_edit.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/save')
def edit_type_one_question():
    try:
        return render_template('type_one_question.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/save')
def save_type_two_question():
    try:
        return render_template('type_two_question.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
def edit_type_one_question_remove():
    try:
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
def edit_type_one_question_remove():
    try:
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()