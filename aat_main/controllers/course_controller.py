from flask import Blueprint, render_template
from flask_login import current_user, login_required

from aat_main import db
from aat_main.models.assessment_models import Assessment

course_bp = Blueprint('course_bp', __name__)


# Make login required for all endpoints within blueprint
@course_bp.before_request
@login_required
def before_request():
    pass


@course_bp.route('/course/')
def course_page():
    return render_template('course.html')


@course_bp.route('/course/assessment/')
def course_assessment_page():
    return render_template('assessment.html')


@course_bp.route('/completed_assessments/')
def completed_assessments():
    assessments = current_user.get_completed_assessments()
    print(assessments)
    return render_template('completed_assessments.html', assessments=assessments)


@course_bp.route('/assessments/')
def assessments():
    if current_user.role == 'student':
        return render_template('assessments_students.html')
    elif current_user.role == 'lecturer':
        assessments = db.session.query(Assessment).all()
        return render_template('assessments_lecturers.html', assessments=assessments)

    return render_template('base.html')


# Assessments Management page (Matt)
@course_bp.route('/assessments/assessments_management/')
@login_required
def assessments_management():
    return render_template('assessments_management.html')
