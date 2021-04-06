from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, RadioField
from aat_main.models.question_models import Question


class assessment_form(FlaskForm):
    QUESTIONS_CHOICES = {}
    questions = Question.get_questions()
    for question in questions:
        QUESTIONS_CHOICES[question.id] = question.name

    title = TextAreaField('Assessment Title')
    questions = SelectField("Questions: ", choices=QUESTIONS_CHOICES.values())
    course = RadioField("Course: ", choices=["Course 1", "Course 2"])
    description = TextAreaField('Assessment Description')
    submit = SubmitField('Submit')
