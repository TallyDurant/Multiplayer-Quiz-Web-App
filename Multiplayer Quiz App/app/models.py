from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email         = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)
    quiz_complete = db.relationship('QuizComplete', backref='userId', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Quiz(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    quiz_name    = db.Column(db.String(100), nullable=False)
    quiz_details = db.Column(db.String(300))
    date_posted  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    question_set = db.relationship('Question', backref='quizName')
    answer_key   = db.relationship('Answer', backref='quizName')
    attempt      = db.relationship('QuizAttempt', backref='quizattempt')
    def __repr(self):
        return '<Post {}>'.format(self.quiz_name)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    #Mult_choice = db.column(db.Boolean, nullable=False)
    quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    #options = db.Column(db.String)
    answer_set = db.relationship('Answer', backref='questionName')

    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    correct = db.Column(db.Boolean, default=False)
    questions = db.Column(db.Integer, db.ForeignKey('question.id'))
    quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    
class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    attempt_string = db.Column(db.String(), nullable=False)

class QuizComplete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    score = db.Column(db.Integer, nullable=False)
