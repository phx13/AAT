from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from aat_main.models.question_models import Question

question_bp = Blueprint('question_bp', __name__, template_folder='../views/question', url_prefix='/question')


@question_bp.route('/management/')
def manage_questions():
    # TODO this is just to test functionality. implement it properly so that is only shows questions that the lecturer
    #   should see (questions from their module)
    # questions = current_user.get_available_questions()
    # questions = Question.get_all()
    modules = current_user.get_enrolled_modules()
    return render_template('question_management.html', modules=modules)


@question_bp.route('/management/data/<string:module>', methods=['GET'])
def question_data(module):
    try:
        if module == 'All':
            origin_data = Question.get_question_by_all_module()
        else:
            origin_data = Question.get_question_by_module(module)
        data = []
        type_dic = {0: 'formative-type-one', 1: 'formative-type-two', 2: 'summative'}
        for od in origin_data:
            dic = {
                'id': od.id,
                'module': od.module_code,
                'question': od.name,
                'description': od.description,
                'type': type_dic[od.type],
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


@question_bp.route('/management/data/delete/', methods=['POST'])
def delete_question():
    try:
        for k, v in request.form.items():
            Question.delete_question_by_id(k)
        return 'delete successful'
    except:
        return 'Server error'


@question_bp.route('/management/data/create/', methods=['POST'])
def create_question():
    try:
        question = {}
        for k, v in request.form.items():
            question[k] = v
        Question.create_question_management(question['module_code'], question['name'], int(question['type']), question['description'], question['option'], question['answer'])
        return 'create successful'
    except:
        return 'server error'


@question_bp.route('/management/data/edit/', methods=['POST'])
def edit_question():
    try:
        return 'edit successful'
    except:
        return 'server error'


@question_bp.route('/completed/')
def completed_questions():
    questions = current_user.get_completed_questions()
    return render_template('completed_questions.html', questions=questions)

# @question_bp.route('/course/assessment/<int:assessment_id>')
# def assessment_page():
#     try:
#         return render_template('assessment.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>')
# def type_one_question_page():
#     try:
#         return render_template('type_one_question.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>')
# def type_two_question_page():
#     try:
#         return render_template('type_two_question.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/edit')
# def edit_type_one_question_edit_page():
#     try:
#         return render_template('type_one_question_edit.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/edit')
# def edit_type_two_question_edit_page():
#     try:
#         return render_template('type_two_question_edit.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/save')
# def edit_type_one_question():
#     try:
#         return render_template('type_one_question.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/fillinblank<question_id>/save')
# def save_type_two_question():
#     try:
#         return render_template('type_two_question.html')
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
# def edit_type_one_question_remove():
#     try:
#         return redirect(url_for('assessment_page'))
#     except TemplateError:
#         raise NotFoundException()
#
#
# @question_bp.route('/course/assessment/<int:assessment_id>/multiplechoice<question_id>/remove')
# def edit_type_two_question_remove():
#     try:
#         return redirect(url_for('assessment_page'))
#     except TemplateError:
#         raise NotFoundException()
