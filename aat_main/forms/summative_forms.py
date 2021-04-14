from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired
from aat_main.models.module_model import Module




class assessment_form(FlaskForm):
    MODULE_CHOICES = {}
    modules = Module.get_all()
    for module in modules:
        MODULE_CHOICES[module.code + "  :  " +module.name] = module.code 

    title = TextAreaField('Assessment Title', validators=[DataRequired()])
    # Course will be changed to only show courses that each lecturer is on. 
    module = SelectField('Modules: ', choices=MODULE_CHOICES)
    description = TextAreaField('Assessment Description', validators=[DataRequired()])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    submit = SubmitField()

