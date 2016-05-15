from flask import render_template, jsonify, flash, redirect, url_for, session, request, abort
from app import app, db, bcrypt, mail
from flask_login import login_user, logout_user
from .forms import LoginForm, RegisterForm, SettingsForm
from .models import User, Task, Admin
from flask_mail import Message
import security
import re
import requests

#---- Helper space

global form_errors
form_errors = None

#This function is here to help me validate login, and keep the login view simple and clean, and is made because wtforms is not efficient enough when validating forms
def validate_login(form):
	req_email = form.email.data
	req_password = form.password.data
	user = User.query.filter_by(email=req_email).first()
	if user is None:
		print "Fake email"
		return "Email is incorrect"
	elif not bcrypt.check_password_hash(user.password, req_password):
		return "Password is incorrect"
	else:
		return None

def validate_register(form):
	req_name = form.first_name.data
	req_email = form.email.data
	req_password = form.password.data
	req_password_again = form.password_again.data
	u = User.query.filter_by(email=req_email).first()


	if req_name == "" or req_email == "" or req_password == "":
		return "Please enter all fields"
	elif u != None:
		return "Email is already registered"
	elif req_password != req_password_again:
		return "Passwords don't match"
	elif not re.match("[^@]+@[^@]+\.[^@]+", req_email):
		return "Did you enter a real email address ?"
	else:
		return None

def send_email(email, subject, html):
	key = 'key-d7cf59282e21d2143d887118d0996aac'
	sandbox = 'sandbox0b7960a242c44b94a9c62ad543335a03.mailgun.org'
	recipient = email
	body = html

	request_url='https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
	request = requests.post(request_url, auth=('api', key), data={
		'from': 'hello@example.com',
		'to': recipient,
		'subject': 'Verify your email please',
		'text': body
	})
	print 'Status: {0}'.format(request.status_code)
	print 'Body: {}'.format(request.text)


#---- Actual views below

@app.route('/')
def index():
	global form_errors
	error = form_errors
	form_errors = None
	lform = LoginForm()
	rform = RegisterForm()
	return render_template('index.html', lform=lform, rform=rform, error = error)

@app.route('/login', methods=['POST'])
def login():
	global form_errors
	lform = LoginForm()
	rform = RegisterForm()
	form_errors = validate_login(lform)
	if form_errors == None:
		user = User.query.filter_by(email=lform.email.data).first()
		login_user(user)
		return redirect(url_for('home'))
	else:
		return redirect(url_for('index'))



@app.route('/register', methods=['POST'])
def register():
	global form_errors
	error = form_errors
	lform = LoginForm()
	rform = RegisterForm()
	form_errors = validate_register(rform)
	if form_errors == None:
		user = User(first_name=rform.first_name.data, email=rform.email.data, password=rform.password.data)
		req_email = rform.email.data
		db.session.add(user)
		db.session.commit()



		subject = "Confirm your email"
		token = security.ts.dumps(rform.email.data, salt='email-confirm-key')

		confirm_url = url_for('confirm_email', token=token, _external=True)

		html = "confirm email with this link %s" % (confirm_url)

		send_email(req_email, subject, html)

		return redirect(url_for('home'))
	else:
		return redirect(url_for('index'))

@app.route('/confirm/<token>')
def confirm_email(token):
	try:
		email = security.ts.loads(token, salt="email-confirm-key", max_age=86400)
	except:
		abort(404)
	user = User.query.filter_by(email=email).first_or_404()
	user.verified = True

	db.session.add(user)
	db.session.commit()

	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/settings')
def settings():
	pass

@app.route('/stats')
def stats():
	pass

@app.route('/admin_login')
def admin_login():
	pass

@app.route('/admin')
def admin():
	pass
