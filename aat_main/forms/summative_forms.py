from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired
from aat_main.models.question_models import Question


class assessment_form(FlaskForm):
    QUESTIONS_CHOICES = {}
    questions = Question.get_questions()
    for question in questions:
        QUESTIONS_CHOICES[question.id] = question.name

    title = TextAreaField('Assessment Title')
    questions = SelectMultipleField("Questions: ", choices=QUESTIONS_CHOICES.items(), validators=[DataRequired()])
    # Course will be changed to only show courses that each lecturer is on. 
    course = RadioField("Course: ", choices=["Course 1", "Course 2"])
    description = TextAreaField('Assessment Description')
    submit = SubmitField()

# Check box instead maybe?
