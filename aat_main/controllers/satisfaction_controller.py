from flask import Blueprint, render_template, redirect, url_for, flash
from aat_main.forms.satisfaction_forms import AssessmentReviewForm
from aat_main.models.satisfaction_models import AssessmentReview
from flask_login import current_user
satisfaction_bp = Blueprint('satisfaction_bp', __name__, url_prefix='/review',
                            template_folder='../views/satisfaction_reviews')


@satisfaction_bp.route('/assessment/<id>', methods=['GET', 'POST'])
def assessment_review(id):
    print(id)
    form = AssessmentReviewForm()
    # reference https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask/14591681#14591681
    #  20 march
    if form.validate_on_submit():
        answers = {'I feel that I had sufficient knowledge to complete this assessment': form.statement1.data,
                   'I found this assessment difficult': form.statement2.data,
                   'COMMENT': form.comment.data}
        # submit answers here
        print(answers)
        AssessmentReview.create_assessment_review(current_user.id, id, form.statement1.data, form.statement2.data,
                                                  form.comment.data)
        # redirect(url_for('satisfaction_bp.assessment_review_complete'))
        return redirect(url_for('satisfaction_bp.assessment_review_complete'))
    else:
        for field, error in form.errors.items():
            for err in error:
                flash(err)  # I decided to flash the errors to the browser

    return render_template('assessment_review.html', assessment_id=id, form=form)


@satisfaction_bp.route('/assessment/complete')
def assessment_review_complete():
    return render_template('assessment_review_complete.html')