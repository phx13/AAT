from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class assessment_form(FlaskForm):
    title = TextAreaField('Assessment Title')
    # description = TextAreaField('Assessment Description')
    submit = SubmitField('Submit')
