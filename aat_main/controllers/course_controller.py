from flask import Blueprint, render_template
from flask_login import current_user, login_required
from aat_main import db
from aat_main.models.assessment_models import Assessment, AssessmentCompletion

course_bp = Blueprint('course_bp', __name__)


@course_bp.route('/course/')
def course_page():
    return render_template('course.html')


@course_bp.route('/course/assessment/')
def course_assessment_page():
    return render_template('assessment.html')


@course_bp.route('/completed_assessments/')
@login_required
def completed_assessments():
    assessments = current_user.get_completed_assessments()
    print(assessments)
    return render_template('completed_assessments.html', assessments=assessments)


@course_bp.route('/assessments/')
@login_required
def assessments():
    return render_template('assessments.html')