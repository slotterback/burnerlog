from flask_wtf import FlaskForm
from wtforms import StringField, Password, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ReportForm(FlaskForm):
    description = StringField('Job Description', validators=[DataRequired()])
    actions = StringField('Action Taken', validators=[DataRequired()])
    recommendations = StringField('Recommendations')
    submit = SubmitField('Submit Report')


