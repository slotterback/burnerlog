from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app.models import Customer


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ReportForm(FlaskForm):
    summary = StringField('Job Description', validators=[DataRequired()])
    action = TextAreaField('Action Taken', validators=[DataRequired()])
    recommendation = TextAreaField('Recommendations')
    submit = SubmitField('Submit Report')

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired()])
    notes = StringField('Notes')
    submit = SubmitField('Ok')


