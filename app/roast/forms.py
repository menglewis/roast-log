# -*- coding: utf-8 -*-
from datetime import datetime
from flask import flash
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Optional


class BeanForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')


class RoasterForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')


class RoastForm(Form):
    bean = SelectField('Bean', validators=[DataRequired()])
    roaster = SelectField('Roaster', validators=[DataRequired()])

    start_time = StringField('Start Time', validators=[DataRequired()])
    start_temp = IntegerField('Start Temperature (F)', validators=[Optional()])
    start_weight = IntegerField('Start Weight (g)', validators=[Optional()])

    fc_start_time = StringField('Start Time')
    fc_start_temp = IntegerField('Start Temperature (F)', validators=[Optional()])
    fc_end_time = StringField('End Time')
    fc_end_temp = IntegerField('End Temperature (F)', validators=[Optional()])

    sc_start_time = StringField('Start Time')
    sc_start_temp = IntegerField('Start Temperature (F)', validators=[Optional()])
    sc_end_time = StringField('End Time')
    sc_end_temp = IntegerField('End Temperature (F)', validators=[Optional()])

    end_time = StringField('End Time', validators=[DataRequired()])
    end_temp = IntegerField('End Temperature (F)', validators=[Optional()])
    end_weight = IntegerField('End Weight (g)', validators=[Optional()])

    roast_datetime = StringField('Roast Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')


def flash_form_errors(form, category="warning"):
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)
