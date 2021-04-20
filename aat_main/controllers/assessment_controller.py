from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

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
        assessments = current_user.get_available_assessments()
        return render_template('assessments_lecturers.html', assessments=assessments)

    return render_template('base.html')


@assessment_bp.route('/upcoming/')
def upcoming_assessments():
    if current_user.role == 'student':
        assessments = Assessment.get_all()
        return render_template('upcoming_assessments.html', assessments=assessments)

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
    return render_template('assessments_management.html')


@assessment_bp.route('/<assessment_id>/questions')
def assessment_questions(assessment_id):
    assessment = Assessment.get_assessment_by_id(assessment_id)
    questions = assessment.get_questions()
    return render_template('assessment_questions.html', assessment=assessment, questions=questions)
