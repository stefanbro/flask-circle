from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64))
	email = db.Column(db.String(64), unique=True)
	_password = db.Column(db.String(128))
	verified = db.Column(db.Boolean, default=False)
	task_time = db.Column(db.Integer, default=45)
	short_break = db.Column(db.Integer, default=5)
	long_break = db.Column(db.Integer, default=15)
	before_short_break = db.Column(db.Integer, default=3)	
	tasks = db.relationship('Task', backref='user', lazy='dynamic')
	
	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)
	
	def __repr__(self):
		return '<User %r>'
	

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	total_time = db.Column(db.Integer, default=0)
	total_this_week = db.Column(db.Integer, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Task %r>' % (self.body)
	
class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64))
	password = db.Column(db.Integer)
	greeting = db.Column(db.String(64))
	
