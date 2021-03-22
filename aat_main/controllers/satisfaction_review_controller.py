from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from aat_main.forms.satisfaction_forms import AssessmentReviewForm, AATReviewForm
from aat_main.models.satisfaction_review_models import AssessmentReview, AATReview
from aat_main.models.assessment_models import Assessment

satisfaction_review_bp = Blueprint('satisfaction_review_bp', __name__, url_prefix='/review',
                                   template_folder='../views/satisfaction_reviews')


@satisfaction_review_bp.route('/assessment/<id>', methods=['GET', 'POST'])
def assessment_review(id):
    form = AssessmentReviewForm()
    # reference https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask/14591681#14591681
    #  20 march
    if form.validate_on_submit():
        AssessmentReview.create_review(current_user.id, id, form.statement1.data, form.statement2.data,
                                       form.comment.data)
        return redirect(url_for('satisfaction_review_bp.assessment_review_complete'))
    else:
        for error in form.errors.values():
            flash(error)
    assessment = Assessment.get_assessment_by_id(id)
    return render_template('assessment_review.html', assessment=assessment, form=form)


@satisfaction_review_bp.route('/assessment/complete')
def assessment_review_complete():
    return render_template('assessment_review_complete.html')


@satisfaction_review_bp.route('/aat', methods=['GET', 'POST'])
def aat_review():
    form = AATReviewForm()
    if form.validate_on_submit():
        AATReview.create_review(current_user.id, form.statement1.data, form.statement2.data, form.comment.data)
        flash('Thanks for leaving a review!')
        return redirect(url_for('index_bp.home'))
    else:
        for error in form.errors.values():
            flash(error)
    return render_template('aat_review.html', form=form)
