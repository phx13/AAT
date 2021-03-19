from flask import Blueprint, render_template

course_bp = Blueprint('course_bp', __name__)


@course_bp.route('/course/')
def course_page():
    return render_template('course.html')


@course_bp.route('/course/assessment/')
def course_assessment_page():
    return render_template('assessment.html')
