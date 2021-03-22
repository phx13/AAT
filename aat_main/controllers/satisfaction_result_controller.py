from flask import Blueprint, render_template
from aat_main.models.assessment_models import Assessment

satisfaction_result_bp = Blueprint('satisfaction_result_bp', __name__, url_prefix='/review/results',
                                   template_folder='../views/satisfaction_results')


@satisfaction_result_bp.route('/assessment/<id>', methods=['GET', 'POST'])
def assessment_review_results(id):
    assessment = Assessment.get_assessment_by_id(id)
    return render_template('assessment_review_result.html', assessment=assessment)


@satisfaction_result_bp.route('/aat', methods=['GET', 'POST'])
def aat_review():
    return render_template('aat_review_result.html')
