from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class AssessmentReviewForm(FlaskForm):
    comment = TextAreaField('Additional comments (optional)')
    submit = SubmitField('Submit')
