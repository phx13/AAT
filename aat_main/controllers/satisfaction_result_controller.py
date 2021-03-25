from statistics import mean

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

    responses = {1: 'Strongly disagree', 2: 'Disagree', 3: 'Neither agree nor disagree', 4: 'Agree', 5: 'Strongly agree'}
    statement_responses = [review.statement_response_map for review in reviews]

    statement_counts = SerializationHelper.decode(statement_responses, responses)
    # TODO maybe add mentimeter-style visualization (including mean?)
    comments = [r.comment for r in reviews if r.comment]
    return render_template('assessment_review_result.html', assessment=assessment, results=statement_counts,
                           comments=comments)


@satisfaction_result_bp.route('/aat', methods=['GET', 'POST'])
def aat_review_results():
    # statements = [
    #     'I find it easy to navigate the AAT to find my tasks that need to be completed',
    #     'I am pleased overall with the functionality of the AAT'
    # ]
    # responses = ['Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree']
    # reviews = db.session.query(AATReview).all()
    # statement_answers = [
    #     [review.statement1_answer for review in reviews],
    #     [review.statement2_answer for review in reviews]
    # ]
    #
    # # reference https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points/455634#455634. 22 March
    # means = ['{:.2f}'.format(mean(answers)) for answers in statement_answers]
    #
    # # this creates a list of sublists, where each sublist is made up of tuples of the form (response, count),
    # # e.g ('Disagree', 2). So each sublist contains the frequency of each response for a specific statement. And so
    # # values_list contains the frequency of each response for all statements
    # response_counts = [[s.count(1), s.count(2), s.count(3), s.count(4), s.count(5)] for s in statement_answers]
    # values_list = [zip(responses, rc) for rc in response_counts]
    reviews = AATReview.get_all_reviews()
    responses = {1: 'Strongly disagree', 2: 'Disagree', 3: 'Neither agree nor disagree', 4: 'Agree', 5: 'Strongly agree'}
    statement_responses = [review.statement_response_map for review in reviews]
    statement_counts = SerializationHelper.decode(statement_responses, responses)
    # TODO maybe add mentimeter-style visualization (including mean?)

    comments = [r.comment for r in reviews if r.comment]

    return render_template('aat_review_result.html', results=statement_counts, comments=comments)
