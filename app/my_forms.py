from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields import DateField, RadioField
from app.models import User, Test, Question, Answers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    patronumic = StringField('Patronumic', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CreateTest(FlaskForm):
    testname = StringField('Name of test', validators=[DataRequired()])
    submit = SubmitField('CreateTest')

    def validate_testname(self, testname):
        test = Test.query.filter_by(name=testname.data).first()
        if test is not None:
            raise ValidationError('Please use a different name for test.')

class AddQuestion(FlaskForm):
    test = StringField('Name of test', validators=[DataRequired()])
    body = StringField('Text of question', validators=[DataRequired()])
    answer_name1 = StringField('First answer', validators=[DataRequired()])
    value_answer1 = BooleanField('Right answer')
    answer_name2 = StringField('Second answer', validators=[DataRequired()])
    value_answer2 = BooleanField('Right answer')
    answer_name3 = StringField('Third answer', validators=[DataRequired()])
    value_answer3 = BooleanField('Right answer')
    answer_name4 = StringField('Fourth answer', validators=[DataRequired()])
    value_answer4 = BooleanField('Right answer')
    add_question = SubmitField('Add question')

    def validate_test(self, test):
        tests = Test.query.filter_by(name=test.data).first()
        if tests is None:
            raise ValidationError('That test is not exist.')

class GoTest(FlaskForm):
    i = 0
    list_tests = [('','')]*len(Test.query.all())
    for test in Test.query.all():
        list_tests[i] = (test.id, test.name)
        i = i + 1
    tests = RadioField('test', choices=list_tests)
    start = SubmitField('Start Test')

class AnswerForms(FlaskForm):
    Answer1 = BooleanField()
    Answer2 = BooleanField()
    Answer3 = BooleanField()
    Answer4 = BooleanField()
    SubmitAnswer = SubmitField('Next')