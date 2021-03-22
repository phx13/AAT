from statistics import mean, mode

from flask import Blueprint, render_template

from aat_main import db
from aat_main.models.assessment_models import Assessment
from aat_main.models.satisfaction_review_models import AATReview
from aat_main.utils.authorization_helper import check_if_authorized

satisfaction_result_bp = Blueprint('satisfaction_result_bp', __name__, url_prefix='/review/results',
                                   template_folder='../views/satisfaction_results')

authorized_role = 'lecturer'


@satisfaction_result_bp.route('/assessment/<id>', methods=['GET', 'POST'])
def assessment_review_results(id):
    check_if_authorized(authorized_role)
    assessment = Assessment.get_assessment_by_id(id)
    return render_template('assessment_review_result.html', assessment=assessment)


@satisfaction_result_bp.route('/aat', methods=['GET', 'POST'])
def aat_review():
    check_if_authorized(authorized_role)


    statements = [
        'I find it easy to navigate the AAT to find my tasks that need to be completed',
        'I am pleased overall with the functionality of the AAT'
    ]
    responses = ['Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree']
    reviews = db.session.query(AATReview).all()
    s_answers = [
        [r.statement1_answer for r in reviews],
        [r.statement2_answer for r in reviews]
    ]

    # reference https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points/455634#455634. 22 March
    means = ['{:.2f}'.format(mean(answers)) for answers in s_answers]

    values_list = [[s.count(1), s.count(2), s.count(3), s.count(4), s.count(5)] for s in s_answers]
    values_list = [zip(responses, v) for v in values_list]

    comments = [r.comment for r in reviews if r.comment]

    return render_template('aat_review_result.html', results=zip(statements, means), comments=comments,
                           response_counts=values_list)
