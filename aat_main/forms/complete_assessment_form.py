from flask_wtf import FlaskForm
from aat_main import db
from wtforms import SubmitField, RadioField

class complete_assessment_form(FlaskForm):
    submit = SubmitField()