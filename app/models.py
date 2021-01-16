from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    patronumic = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    results = db.relationship('UserResults', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True)
	questions = db.relationship('Question', backref='mame_of_test', lazy='dynamic')

	def __repr__(self):
		return '<Test: {}>'.format(self.name)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(256))
	type = db.Column(db.Integer, default=1)
	test = db.Column(db.Integer, db.ForeignKey('test.id'))
	answers = db.relationship('Answers', backref='name_of_question', lazy='dynamic')

	def __repr__(self):
		return 'Question: {}'.format(self.body)

class Answers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(128))
	value = db.Column(db.Boolean)
	quest = db.Column(db.Integer, db.ForeignKey('question.id'))

	def __resp__(self):
		return 'Answer: {}'.format(self.body)

class UserAnswers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'))
	question = db.Column(db.Integer, db.ForeignKey('question.id'))
	answers = db.Column(db.Integer, db.ForeignKey('answers.id'))

class UserResults(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	u_res = db.Column(db.Integer, db.ForeignKey('user.id'))
	t_res = db.Column(db.Integer, db.ForeignKey('test.id'))
	result = db.Column(db.Float(10))
	max = db.Column(db.Float(10))
	right = db.Column(db.Float(10))
	error = db.Column(db.Float(10))
		