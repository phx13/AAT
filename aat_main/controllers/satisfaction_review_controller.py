import json

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from aat_main.forms.satisfaction_forms import AssessmentReviewForm, AATReviewForm, QuestionReviewForm
from aat_main.models.assessment_models import Assessment
from aat_main.models.question_models import Question
from aat_main.models.satisfaction_review_model import AssessmentReview, AATReview, QuestionReview
from aat_main.utils.authorization_helper import check_if_authorized

satisfaction_review_bp = Blueprint('satisfaction_review_bp', __name__, url_prefix='/review',
                                   template_folder='../views/satisfaction_reviews')

authorized_role = 'student'


@satisfaction_review_bp.route('/assessment/<assessment_id>', methods=['GET', 'POST'])
def assessment_review(assessment_id):
    check_if_authorized(authorized_role)

    form = AssessmentReviewForm()
    # reference https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask/14591681#14591681
    #  20 march
    if form.validate_on_submit():
        statement_response_map = json.dumps(
            {
                form.statement1.label.text: form.statement1.data,
                form.statement2.label.text: form.statement2.data
            }
        )

        AssessmentReview.create_review(current_user.id, assessment_id, statement_response_map, form.comment.data)
        return redirect(url_for('satisfaction_review_bp.assessment_review_complete'))
    else:
        for error in form.errors.values():
            flash(error)
    assessment = Assessment.get_assessment_by_id(id)
    return render_template('assessment_review.html', assessment=assessment, form=form)


@satisfaction_review_bp.route('/assessment/complete')
def assessment_review_complete():
    check_if_authorized(authorized_role)
    return render_template('assessment_review_complete.html')


@satisfaction_review_bp.route('/aat', methods=['GET', 'POST'])
def aat_review():
    check_if_authorized(authorized_role)

    form = AATReviewForm()
    if form.validate_on_submit():
        # TODO restructure program to allow for more statements to be added to forms and answers to be stored easily
        # reference 30 march. https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
        # reference 30 march. https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify
        statement_response_map = json.dumps(
            {
                form.statement1.label.text: form.statement1.data,
                form.statement2.label.text: form.statement2.data
            }
        )

        AATReview.create_review(current_user.id, statement_response_map, form.comment.data)
        flash('Thanks for leaving a review!')
        return redirect(url_for('index_bp.home'))
    else:
        for error in form.errors.values():
            flash(error)
    return render_template('aat_review.html', form=form)


@satisfaction_review_bp.route('/question/<question_id>', methods=['GET', 'POST'])
def question_review(question_id):
    check_if_authorized(authorized_role)
    form = QuestionReviewForm()
    if form.validate_on_submit():
        statement_response_map = json.dumps(
            {
                form.statement1.label.text: form.statement1.data,
                form.statement2.label.text: form.statement2.data
            }
        )
        QuestionReview.create_review(current_user.id, question_id, statement_response_map, form.comment.data)
        return redirect(url_for('satisfaction_review_bp.question_review_complete'))
    else:
        for error in form.errors.values():
            flash(error)

    question = Question.get_question_by_id(question_id)
    return render_template('question_review.html', question=question, form=form)


@satisfaction_review_bp.route('/question/complete')
def question_review_complete():
    check_if_authorized(authorized_role)
    return render_template('question_review_complete.html')
