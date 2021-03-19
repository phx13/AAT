from flask import Blueprint, render_template

satisfaction_bp = Blueprint('satisfaction_bp', __name__, url_prefix='/review', template_folder='views/satisfaction')


@satisfaction_bp.route('/assessment/<id>')
def assessment_review(id):
    print(id)
    return render_template('assessment_review.html', assessment_id=id)
