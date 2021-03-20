from flask import Blueprint, render_template
from aat_main import db

course_bp = Blueprint('course_bp', __name__)


@course_bp.route('/course/')
def course_page():
    return render_template('course.html')


@course_bp.route('/course/assessment/')
def course_assessment_page():
    return render_template('assessment.html')


@course_bp.route('/completed_assessments/')
def completed_assessments():
    # assessments =
    return render_template('completed_assessments.html')


@course_bp.route('/assessments/')
def assessments():
    return render_template('assessments.html')