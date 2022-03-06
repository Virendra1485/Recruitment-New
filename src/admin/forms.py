from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, IntegerField, SubmitField, PasswordField, TextAreaField, SelectField, \
    BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdminRegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    mobile_no = StringField('Mobile No', validators=[DataRequired(), Length(min=10, max=10)])
    email_id = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LogInForm(FlaskForm):
    email_id = StringField('Email ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')