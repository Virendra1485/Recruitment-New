from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, IntegerField, SubmitField, PasswordField, TextAreaField, SelectField, \
    BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CandidateRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email_id = StringField('Email', validators=[DataRequired(), Email()])
    mobile_no = StringField('Mobile No', validators=[DataRequired(), Length(min=10, max=10)])
    state = SelectField('State', choices=['Select', 'Madhya Pradesh', 'Uttar Pradesh', 'Maharastra'])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    ssc_board = StringField('10th Board', validators=[DataRequired(), Length(min=2, max=20)])
    ssc_marks = IntegerField('SSC Marks', validators=[DataRequired()])
    hsc_board = StringField('12th Board', validators=[DataRequired(), Length(min=2, max=20)])
    hsc_marks = IntegerField('HSC Marks', validators=[DataRequired()])
    ug_degree = StringField('UG Course Name', validators=[DataRequired(), Length(min=2, max=25)])
    ug_college = StringField('UG College Name', validators=[DataRequired(), Length(max=50)])
    ug_university = StringField('UG University Name', validators=[DataRequired(), Length(max=50)])
    ug_marks = IntegerField('UG Marks')
    pg_degree = StringField('PG Course Name')
    pg_college = StringField('PG College Name')
    pg_university = StringField('PG University Name')
    pg_marks = IntegerField('PG Marks', default=0)
    skill = TextAreaField('Technical Proficency')
    linked_link = StringField('Linkedin Link')
    skype_id = StringField('Skype Id')
    resume_remark = TextAreaField('Resume Remark')
    resume = FileField('Resume', validators=[FileAllowed(['txt', 'pdf'], 'only txt file alowed')])
    submit = SubmitField('Register')


class LogInForm(FlaskForm):
    email_id = StringField('Email ID', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TestForm(FlaskForm):
    options = RadioField()