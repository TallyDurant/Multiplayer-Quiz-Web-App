from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import *

class RegistrationForm(FlaskForm):
    username            = StringField('Username', 
                            validators= [DataRequired(), Length(min=2,max=20)])
    email               = StringField('Email', 
                            validators= [DataRequired(), Email()])
    password            = PasswordField('Password',
                            validators= [DataRequired()])
    confirm_password    = PasswordField('Comfirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit              = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')

class LoginForm(FlaskForm):
    username    = StringField('Username', validators = [DataRequired()])
    password    = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Login')

class QuestionsAnswers(FlaskForm):
    
    #quesType = SelectField("Type", choices = [("shortAns", "Short Answer"), ("longAns", "Long Answer"), ("multi", "Multi-Choice")])
    quizQuestion = StringField("Question: ", validators=[DataRequired()])
    #quizAnswer = StringField("Answer: ")
    option1 = StringField("Wrong Answer: ")
    option2 = StringField("Wrong Answer: ")
    option3 = StringField("Wrong Answer: ")
    # Add Validation

class QuestionAdd(Form):
    # subform to be called when adding new questions and answers
    quizQuestion = StringField("Question: ", validators=[DataRequired()])
    quizAnswer = StringField("Answer: ")
    option1 = StringField("Wrong Answer: ")
    option2 = StringField("Wrong Answer: ")
    option3 = StringField("Wrong Answer: ")

    
class QuizCreation(FlaskForm):
    quiz_name = StringField("Quiz Name: ", validators=[DataRequired()])
    quiz_details = StringField("Quiz Details")
    #myChoices = [1,2,3,4,5,6,7,8,9,10]
    #numQues = SelectField("Number of Questions", choices = myChoices, validators = [DataRequired()]) 
    question = FieldList(FormField(QuestionAdd), min_entries=1, max_entries=10)  
    # quizQuestion = StringField("Question: ", validators=[DataRequired()])
    # quizAnswer = StringField("Answer: ")
    # option1 = StringField("Option: ")
    # option2 = StringField("Option: ")
    # option3 = StringField("Option: ")
    submit = SubmitField('Create Quiz')

    # def validate_quizName(self, quizName):
    #     quiz = Quiz.query.filter_by(quiz_name=quiz_name.data).first()
    #     if quiz is not None:
    #         raise ValidationError('Quiz Name already taken')



class QuizForm(FlaskForm):
    jsonString = StringField('JSON String', validators=[DataRequired()])
    submit = SubmitField('Submit')

class QuizScore(FlaskForm):
    score = DecimalField('Score', validators=[DataRequired()])
    submit = SubmitField('Submit Score')