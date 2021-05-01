from flask_wtf import FlaskForm

from aat_main import db


from wtforms import SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Length
from aat_main.models.module_model import Module
from aat_main.models.enrolment_models import ModuleEnrolment
from aat_main.models.account_model import AccountModel



class assessment_form(FlaskForm):
    def validate_module(form, module):
        if module.data == "Please Choose a Module":
            raise ValidationError("Please Choose a Module!")

    title = TextAreaField('Assessment Title', validators=[DataRequired(), Length(min=5, max=64)])
    # Course will be changed to only show courses that each lecturer is on. 
    module = SelectField(choices=[], default="Please choose a module")
    description = TextAreaField('Assessment Description', validators=[DataRequired(), Length(min=0, max=512)])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    timelimit = IntegerField("Minutes")
    submit = SubmitField()


class summative_edit_form(FlaskForm):
    submit = SubmitField()



    

