from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from jinja2 import TemplateError
from sqlalchemy.exc import SQLAlchemyError

from aat_main.models.question_models import QuestionData
from aat_main.utils.api_exception_helper import NotFoundException, InterServerErrorException

question_bp = Blueprint('question_bp', __name__, template_folder='../views/question')


@question_bp.route('/question/management/')
def question_page():
    try:
        return render_template('question_management.html')
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/question/management/data/', methods=['GET'])
def question_data():
    try:
        origin_data = QuestionData.search_all()
        data = []
        for od in origin_data:
            dic = {}
            dic['id'] = od.id
            dic['course'] = od.course
            dic['question'] = od.question
            dic['option'] = od.option
            dic['answer'] = od.answer
            dic['release_time'] = od.release_time
            data.append(dic)
        if request.method == 'GET':
            info = request.values
            limit = info.get('limit', 10)
            offset = info.get('offset', 0)
        return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    except TemplateError:
        raise NotFoundException()


@question_bp.route('/question/management/data/', methods=['POST'])
def delete_question_data():
    try:
        for k,v in request.form.items():
            QuestionData.delete_question_by_id(k)
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
