from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
import json
import random

from aat_main.models.assessment_models import Assessment

assessment_bp = Blueprint('assessment_bp', __name__, url_prefix='/assessments')


# Make login required for all endpoints within blueprint
@assessment_bp.before_request
@login_required
def before_request():
    pass


@assessment_bp.route('/')
def assessments():
    if current_user.role == 'student':
        return render_template('assessments_students.html')
    elif current_user.role == 'lecturer':
        # assessments = db.session.query(Assessment).all()
        assessments = current_user.get_available_assessments_lecturer()
        return render_template('assessments_lecturers.html', assessments=assessments)

    return render_template('base.html')


@assessment_bp.route('/available/')
def available_assessments():
    if current_user.role == 'student':
        assessments = current_user.get_available_assessments_student()

        return render_template('available_assessments.html', assessments=assessments)

    return redirect(url_for('assessment_bp.assessments'))


@assessment_bp.route('/completed/')
def completed_assessments():
    assessments = current_user.get_completed_assessments()
    print(assessments)
    return render_template('completed_assessments.html', assessments=assessments)


# Assessments Management page (Matt)
@assessment_bp.route('/manage')
@login_required
def assessments_management():
    assessments = Assessment.get_all()
    return render_template('assessments_management.html', assessments=assessments)


# @assessment_bp.route('/<assessment_id>/questions')
# def assessment_questions(assessment_id):
#     assessment = Assessment.get_assessment_by_id(assessment_id)
#     questions = assessment.get_questions()
#     return render_template('assessment_questions.html', assessment=assessment, questions=questions)

@assessment_bp.route('/<assessment_id>/start')
def start_assessment(assessment_id):
    assessment = Assessment.get_assessment_by_id(assessment_id)
    assessment_questions = json.loads(assessment.questions)
    question_num = 0
    for question in assessment_questions:
        question_num += 1

    random.shuffle(assessment_questions)
    current_question = assessment_questions[0]

    return render_template('assessment_start.html', assessment=assessment,
     assessment_questions=assessment_questions, current_question=current_question)

# @assessment_bp.route('/<assessment_id>/<current_question>')
# def questions_assessment(assessment_id, current_question, assessment_questions):
#     assessment_questions = request.args.get('assessment_questions', None)
#     # on submit, render update db/data_string. render assessment_questions passing data_string, question ids, current questions etc and assessment. 
#     # on submit, if question id = last in list, commit question data to db. Render assessment done page.

#     return render_template('question_in_assessment.html', assessment_id=assessment_id, current_question=current_question, assessment_questions=assessment_questions)
