from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user
import json

from aat_main.forms.satisfaction_forms import AssessmentReviewForm, AATReviewForm
from aat_main.models.assessment_models import Assessment
from aat_main.models.satisfaction_review_models import AssessmentReview, AATReview
from aat_main.utils.authorization_helper import check_if_authorized
from aat_main.utils.serialization_helper import SerializationHelper

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
        # TODO find way to use list of dicts here instead of janky string
        # statement_response_map = f'{form.statement1.label.text},{form.statement1.data}+' +\
        #                          f'{form.statement2.label.text},{form.statement2.data}'
        # print(statement_response_map)
        statement_response_map = SerializationHelper.encode(
            (form.statement1.label.text, form.statement1.data),
            (form.statement2.label.text, form.statement2.data)
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
        # https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
        # qa_map = {
        #     form.statement1.label: form.statement1.data,
        #     form.statement2.label: form.statement2.data
        # }
        statement_response_map = SerializationHelper.encode(
            (form.statement1.label.text, form.statement1.data),
            (form.statement2.label.text, form.statement2.data)
        )

        AATReview.create_review(current_user.id, statement_response_map, form.comment.data)
        flash('Thanks for leaving a review!')
        return redirect(url_for('index_bp.home'))
    else:
        for error in form.errors.values():
            flash(error)
    return render_template('aat_review.html', form=form)
