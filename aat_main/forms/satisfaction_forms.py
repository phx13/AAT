from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField


class ReviewForm(FlaskForm):
    options = [
        (1, 'Strongly disagree'),
        (2, 'Disagree'),
        (3, 'Neither agree nor disagree'),
        (4, 'Agree'),
        (5, 'Strongly Agree')
    ]
    comment = TextAreaField('Additional comments (optional)')
    submit = SubmitField('Submit')


class AssessmentReviewForm(ReviewForm):
    statement1 = RadioField('I feel that I had sufficient knowledge to complete this assessment',
                            choices=ReviewForm.options)
    statement2 = RadioField('I found this assessment difficult', choices=ReviewForm.options)


class AATReviewForm(ReviewForm):
    statement1 = RadioField('I find it easy to navigate the AAT to find my tasks that need to be completed',
                            choices=ReviewForm.options)
    statement2 = RadioField('I am pleased overall with the functionality of the AAT', choices=ReviewForm.options)
