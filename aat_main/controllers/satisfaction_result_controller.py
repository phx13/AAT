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

    reviews = db.session.query(AATReview).all()
    s1_answers = [r.statement1_answer for r in reviews]
    s2_answers = [r.statement2_answer for r in reviews]

    s1_mean = '{:.2}'.format(mean(s1_answers))
    s1_mode = mode(s1_answers)  # TODO this mode picks first one encountered in s1_answers. decide if we should use
                                #  min(multimode(data)) or max(multimode(data))

    s2_mean = '{:.2}'.format(mean(s2_answers))
    s2_mode = mode(s2_answers)

    means = [s1_mean, s2_mean]
    modes = [s1_mode, s2_mode]

    values = [1, 1, 3, 1, 1]
    labels = ['Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree']
    colors = ['red', 'blue', 'green', 'yellow', 'black']

    comments = [r.comment for r in reviews if r.comment]

    statements = [
        'I find it easy to navigate the AAT to find my tasks that need to be completed',
        'I am pleased overall with the functionality of the AAT'
    ]
    results = zip(statements, means, modes)
    print(comments)
    return render_template('aat_review_result.html', results=results, comments=comments, max='10', set=zip(values, labels, colors))