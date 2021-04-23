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
    questions = current_user.get_available_questions()
    # questions = Question.get_all()
    return render_template('question_management.html', questions=questions)


@question_bp.route('/management/data/', methods=['GET'])
def question_data():
    try:
        origin_data = current_user.get_enrolled_modules()
        data = []
        for od in origin_data:
            dic = {
                'id': od.id,
                'module': od.module_code,
                'question': od.question,
                'option': od.option,
                'answer': od.answer,
                'release_time': od.release_time
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
        return 'Server error'


@question_bp.route('/management/data/', methods=['POST'])
def delete_question_data():
    try:
        for k, v in request.form.items():
            Question.delete_question_by_id(k)
        return 'delete successful'
    except:
        return 'Server error'


@question_bp.route('/completed/')
def completed_questions():
    questions = current_user.get_completed_questions()
    return render_template('completed_questions.html', questions=questions)
