from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired
from aat_main.models.question_models import Question


class assessment_form(FlaskForm):
    title = TextAreaField('Assessment Title')
    # Course will be changed to only show courses that each lecturer is on. 
    course = RadioField("Course: ", choices=["Course 1", "Course 2"])
    description = TextAreaField('Assessment Description')
    submit = SubmitField()

# Check box instead maybe?
