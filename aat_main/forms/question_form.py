from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField
from wtforms.validators import Length, DataRequired


class type_one_question_form(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    options = TextAreaField('Options (Separete by newline)', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')


class type_two_question_form(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = TextAreaField('Course', validators=[DataRequired()])
    caseSensitive = BooleanField('Case Senstive')
    submit = SubmitField('Submit')