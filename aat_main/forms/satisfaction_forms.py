from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField


class AssessmentReviewForm(FlaskForm):
    options = [
        (1, 'Strongly disagree'),
        (2, 'Disagree'),
        (3, 'Neither agree nor disagree'),
        (4, 'Agree'),
        (5, 'Strongly Agree')
    ]
    statement1 = RadioField('I feel that I had sufficient knowledge to complete this assessment', choices=options)
    statement2 = RadioField('I found this assessment difficult', choices=options)
    comment = TextAreaField('Additional comments (optional)')
    submit = SubmitField('Submit')
