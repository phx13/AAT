from flask import Blueprint, render_template, flash, request, redirect, url_for
from jinja2 import TemplateError

from aat_main.forms.question_form import type_one_question_form, type_two_question_form
from aat_main.models.type_one_question_model import MultipleChoice
from aat_main.models.type_two_question_model import FillinBlank
from aat_main.utils.api_exception_helper import NotFoundException


question_blueprint = Blueprint('question_blueprint', __name__)


@question_blueprint.route('/course/assessment/<int:assessment_id>', methods=['GET', 'POST'])
def assessment_page():
    try:
        return render_template('assessment.html')
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>', methods=['GET', 'POST'])
def type_one_question_page(question_id):
    question = MultipleChoice.search_question_by_id(question_id)
    try:
        return render_template('type_one_question.html', question = question)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>', methods=['GET', 'POST'])
def type_two_question_page(question_id):
    question = FillinBlank.search_question_by_id(question_id)
    try:
        return render_template('type_two_question.html', question = question)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/edit', methods=['GET', 'POST'])
def edit_type_one_question_edit_page(question_id):
    form = type_one_question_form()
    if form.validate_on_submit():
        MultipleChoice.update_question(id=question_id, question=form.question, answer=form.answer, options=form.options)
    try:
        return render_template('type_one_question_edit.html', form = form)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/edit', methods=['GET', 'POST'])
def edit_type_two_question_edit_page(question_id):
    form = type_two_question_form()
    if form.validate_on_submit():
        FillinBlank.update_question(id=question_id, question=form.question, answer=form.answer, caseSensetive=form.caseSensitive)
    try:
        return render_template('type_two_question_edit.html', form = form)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/new_multiplechoice', methods=['GET', 'POST'])
def edit_type_one_question():
    form = type_one_question_form()
    try:
        if form.validate_on_submit():
            MultipleChoice.create_question(question=form.question, answer=form.answer, options=form.options)
            return render_template('type_one_question.html', form=form)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/new_fillinblank', methods=['GET', 'POST'])
def save_type_two_question():
    form = type_two_question_form()
    try:
        if form.validate_on_submit():
            FillinBlank.create_question(question=form.question, answer=form.answer, caseSensetive=form.caseSensitive)
            return render_template('type_two_question.html', form = form)
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove', methods=['GET', 'POST'])
def edit_type_one_question_remove(question_id):
    try:
        MultipleChoice.delete_question(question_id)
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()

@question_blueprint.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove', methods=['GET', 'POST'])
def edit_type_one_question_remove(question_id):
    try:
        FillinBlank.delete_question(question_id)
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()