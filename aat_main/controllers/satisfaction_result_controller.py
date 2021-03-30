from statistics import mean
from ast import literal_eval
from flask import Blueprint, render_template
from flask_login import login_required

from aat_main import db
from aat_main.models.assessment_models import Assessment
from aat_main.models.satisfaction_review_models import AATReview
from aat_main.utils.authorization_helper import check_if_authorized
from aat_main.utils.serialization_helper import SerializationHelper
satisfaction_result_bp = Blueprint('satisfaction_result_bp', __name__, url_prefix='/review/results',
                                   template_folder='../views/satisfaction_results')


@satisfaction_result_bp.before_request
@login_required
def before_request():
    authorized_role = 'lecturer'
    check_if_authorized(authorized_role)


@satisfaction_result_bp.route('/assessment/<id>', methods=['GET', 'POST'])
def assessment_review_results(id):
    assessment = Assessment.get_assessment_by_id(id)

    reviews = assessment.get_reviews()
    responses = {
        '1': 'Strongly disagree',
        '2': 'Disagree',
        '3': 'Neither agree nor disagree',
        '4': 'Agree',
        '5': 'Strongly agree'
    }

    statement_response_counts = SerializationHelper.decode(reviews, responses)

    # TODO maybe add mentimeter-style visualization (including mean?)
    comments = [review.comment for review in reviews if review.comment]

    return render_template('assessment_review_result.html', assessment=assessment, results=statement_response_counts,
                           comments=comments)


@satisfaction_result_bp.route('/aat', methods=['GET', 'POST'])
def aat_review_results():
    # reference https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points/455634#455634. 22 March
    # means = ['{:.2f}'.format(mean(answers)) for answers in statement_answers]

    reviews = AATReview.get_all_reviews()
    responses = {
        '1': 'Strongly disagree',
        '2': 'Disagree',
        '3': 'Neither agree nor disagree',
        '4': 'Agree',
        '5': 'Strongly agree'
    }
    statement_response_counts = SerializationHelper.decode(reviews, responses)

    # TODO maybe add mentimeter-style visualization (including mean?)

    comments = [review.comment for review in reviews if review.comment]

    return render_template('aat_review_result.html', results=statement_response_counts, comments=comments)
