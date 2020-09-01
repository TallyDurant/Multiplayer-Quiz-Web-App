from flask import render_template, redirect, flash, url_for, request, jsonify, Flask, Markup
from app import app, db, admin, login
from app.forms import LoginForm, RegistrationForm, QuestionsAnswers, QuizCreation, QuestionAdd, QuizForm, QuizScore
from flask_login import current_user, login_user, logout_user, login_required 
from app.models import User, Quiz, Question, Answer, QuizAttempt, datetime, QuizComplete
from werkzeug.urls import url_parse
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import ValidationError, DataRequired, Email
import json
import random
import html
import flask.views
import os
import functools
import flask

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#description page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#choose quiz page + login required
@app.route('/quizSelector')
@login_required
def quizSelector():
    quizzes = Quiz.query.all()
    return render_template('quizSelector.html', title='Select Quiz', quizzes=quizzes)

# register new user
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registerFlask.html', title='Register', form=form)

#login route 
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('loginFLask.html', title='Login', form=form)

#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#profile page top view completed quizes and bio info
@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    quizcomp = QuizComplete.query.filter_by(user_id=user.id)
    quiztotals = QuizComplete.query.all()
    quizs = Quiz.query.all()
    #Test data
    labels = [
    '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '10'
    ]
    #Test data
    values = [
    1,2,3,2,1,4,5,2,1,3,6,8,5,6,9,8,5,4,7,1,1,2,5,6,
    5,6,2,3,6,5,5,8,5,4,2,6,5,7,5,4,5,6,5,4,5,6,5,8,
    5,6,2,5,3,5,4,8,5,4,5,8,7,4,5,6,5,2,5,6,5,2,3,6,
    10
    ]
    bar_labels=labels
    bar_values=values
    count=[]
    for i in range(len(bar_labels)):
        count.append(0)
        for j in values:
            if j == i+1:
                count[i]=count[i]+1
    bar_values=count
    sums=0
    counts=len(values)
    for i in values:
        sums=sums+i
    mean=sums/counts
    sumsquare=0
    for i in values:
        sumsquare=(i-mean)**2
    SD=sumsquare/(counts-1)
    data=[]
    data.append(['Number of scores','Number of players'])
    for i in range(len(bar_labels)):
        data.append([bar_labels[i],bar_values[i]])
    return render_template('profile.html', title='profile', user=user, quizcomp=quizcomp, quizs=quizs, quiztotals=quiztotals, data=data, mean=mean, SD=SD)

# ADD USER, MUST BE ADMIN
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    # CHECK IF ADMIN
    if current_user.is_admin == True:
        form = RegistrationForm()
        if request.method == 'GET':
            return render_template('registerFlask.html', title='Register User',form=form)
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
        
    

# delete account
@app.route('/delete/user/<username>')
@login_required
def delete_Account(username):
    userX = User.query.filter_by(username = username).first()
    db.session.delete(userX)
    db.session.commit()
    return redirect(url_for('index'))

#delete Quiz
@app.route('/delete/quiz/<quiz_id>')
def delete_Quiz(quiz_id):
    if current_user.is_admin == True:
        quizNameX = Quiz.query.filter_by(id = quiz_id).first()
        answers = Answer.query.filter_by(quiz=quiz_id)
        if answers != None:
            for answer in answers:
                db.session.delete(answer)
        questions = Question.query.filter_by(quiz=quiz_id)
        if questions != None:
            for question in questions:
                db.session.delete(question)
        db.session.delete(quizNameX)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#take quiz
@app.route('/takeQuiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def takeQuiz(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    if request.method == 'POST':
        form = QuizForm()
        if form.validate_on_submit():
            answers = form.jsonString.data
            quiz    = Quiz.query.filter_by(id=quiz_id).first()        
            attempt = QuizAttempt(user_id = current_user.id, quiz_id = quiz.id, attempt_string=answers)
            db.session.add(attempt)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            # show the form, it wasn't submitted
            return render_template(url_for('takequiz',id=quiz_id))
    else:
        form= QuizForm()
        user = current_user.username
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        questions = Question.query.filter_by(quiz=quiz_id)
        answers = Answer.query.filter_by(quiz=quiz_id)
        ques2 = []
        for question in questions:
            answer2 = []
            for answer in answers:
                if answer.questions == question.id:
                    answer2.append(answer.answer)
            ques2.append({"question": question.question, "answers": answer2})
        print(ques2)
        return render_template('newjsTakeQuiz.html', user=user, quiz=quiz, questions=questions, answers=answers, form=form, ques=ques2)

@app.route('/createQuiz', methods=['GET','POST'])
@login_required
def createQuiz():
    if current_user.is_admin == True:
        form = QuizCreation()
        if request.method == 'GET':
            return render_template('createQuizNew.html', title='Create Quiz', form=form)
        if form.validate_on_submit():
            quiz = Quiz(quiz_name=form.quiz_name.data, quiz_details=form.quiz_details.data, date_posted=datetime.now())
            db.session.add(quiz)
            db.session.commit()
            quiz = Quiz.query.filter_by(quiz_name = form.quiz_name.data).first()
            for question in form.question.data:
                new_question = Question(question=question["quizQuestion"], quiz=quiz.id)
                db.session.add(new_question)
                db.session.commit()
                id_question = Question.query.filter_by(question=question["quizQuestion"]).first()
                answers1 = Answer(answer=question["quizAnswer"], correct=True, questions=id_question.id, quiz=quiz.id)
                option1 = Answer(answer=question["option1"], correct=False, questions=id_question.id, quiz=quiz.id)
                option2 = Answer(answer=question["option2"], correct=False, questions=id_question.id, quiz=quiz.id)
                option3 = Answer(answer=question["option3"], correct=False, questions=id_question.id, quiz=quiz.id)
                db.session.add(answers1)
                db.session.add(option1)
                db.session.add(option2)
                db.session.add(option3)
                db.session.commit()
            return redirect(url_for('quizSelector'))
    else:
        return redirect(url_for('index'))
    
class Music(flask.views.MethodView):
    
    def get(self):
        songs = os.listdir('app/static/music')
        return flask.render_template("music.html", songs=songs)

app.add_url_rule('/music/',
                 view_func=Music.as_view('music'),
                 methods=['GET'])


# PAGE TO VIEW WHICH QUIZZES NEED TO BE ASSESSED
@app.route('/assess')
def assess():
    if current_user.is_admin == True:
        attempts = QuizAttempt.query.all()
        quizzes = Quiz.query.all()
        users = User.query.all()
        return render_template('admin_home.html', attempts=attempts, quizzes=quizzes, users=users)

# ROUTE TO ASSESS THE QUIZ
@app.route('/assess/<quiz_attempt>', methods=['GET','POST'])
def quiz_assess(quiz_attempt):
    if current_user.is_admin == True:
        if request.method == 'GET':
            form = QuizScore()
            attempt = QuizAttempt.query.filter_by(id=quiz_attempt).first()
            attempts = attempt.attempt_string.split(',')
            quiz = Quiz.query.filter_by(id=attempt.quiz_id).first()
            questions = Question.query.filter_by(quiz=quiz.id)
            answers = Answer.query.filter_by(quiz=quiz.id)
            return render_template('assessquiz.html', form=form, answers=answers, attempt=attempt, attempts=attempts, quiz=quiz, questions=questions)
        if request.method == 'POST':
            form = QuizScore()
            # FINISH THIS
            if form.validate_on_submit:
                attempt = QuizAttempt.query.filter_by(id=quiz_attempt).first()
                user = User.query.filter_by(id=attempt.user_id).first()
                quiz = Quiz.query.filter_by(id=attempt.quiz_id).first()
                quiz_score = QuizComplete(user_id=attempt.user_id, quiz_id=attempt.quiz_id,score=int(form.score.data))
                db.session.add(quiz_score)
                db.session.delete(attempt)
                db.session.commit()
                return redirect(url_for('assess'))
            return redirect(url_for('assess'))
            

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Quiz,db.session))
admin.add_view(ModelView(Question,db.session))
admin.add_view(ModelView(Answer,db.session))
admin.add_view(ModelView(QuizAttempt, db.session))
admin.add_view(ModelView(QuizComplete, db.session))
