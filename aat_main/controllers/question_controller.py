from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from jinja2 import TemplateError

from aat_main.models.question_models import Question
from aat_main.utils.api_exception_helper import NotFoundException

question_bp = Blueprint('question_bp', __name__, template_folder='../views/question', url_prefix='/question')


@question_bp.route('/management/')
def manage_questions():
    # TODO this is just to test functionality. implement it properly so that is only shows questions that the lecturer
    #   should see (questions from their module)
    questions = Question.get_question_by_module(current_user.id)
    return render_template('question_management.html', questions=questions)


@question_bp.route('/management/data/', methods=['GET'])
def question_data():
    try:
        origin_data = Question.get_question_by_module(current_user.id)
        data = []
        for od in origin_data:
            dic = {'id': od.id, 'module': od.module_code, 'question': od.question, 'option': od.option, 'answer': od.answer, 'release_time': od.release_time}
            data.append(dic)
        if request.method == 'GET':
            info = request.values
            limit = info.get('limit', 10)
            offset = info.get('offset', 0)
        return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    except:
        return 'Server error'


@question_bp.route('/management/data/', methods=['POST'])
def delete_question_data():
    try:
        for k, v in request.form.items():
            Question.delete_question_by_id(k)
        return 'delete successful'
    except:
        return 'Server error'


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


@question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
def edit_type_two_question_remove():
    try:
        return redirect(url_for('assessment_page'))
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/review_completed')
def completed_questions():
    questions = current_user.get_completed_questions()
    return render_template('completed_questions.html', questions=questions)
