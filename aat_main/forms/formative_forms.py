from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Length
from aat_main.models.module_model import Module


class module_choice_form(FlaskForm):
    MODULE_CHOICES = {}
    MODULE_CHOICES["Please Choose a Module"] = 0
    modules = Module.get_all()
    for module in modules:
        MODULE_CHOICES[module.code + "  :  " + module.name] = module.code

    def validate_module(form, module):
        if module.data == "Please Choose a Module":
            raise ValidationError("Please Choose a Module!")

    module = SelectField(choices=MODULE_CHOICES)
    submit = SubmitField()





