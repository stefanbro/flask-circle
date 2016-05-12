from flask import render_template, jsonify, flash, redirect, url_for, session, request, abort
from app import app, db, bcrypt
from .forms import LoginForm, RegisterForm, SettingsForm
from .models import User, Task, Admin

#---- Helper space

global login_errors
login_errors = None

global register_errors
register_errors = None

#This function is here to help me validate login, and keep the login view simple and clean, and is made because wtforms is not efficient enough when validating forms
def validate_login(form):
	req_email = form.email.data
	req_password = form.password.data
	user = User.query.filter_by(email=req_email).first()
	if user is None:
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
	
	if not form.validate_on_submit():
		return "Fuck you bich"
	else:
		return "Still fuck you"
	
#---- Actual views below
	
@app.route('/')
def index():
	global login_errors
	error = login_errors
	login_errors = None
	lform = LoginForm()
	rform = RegisterForm()
	return render_template('index.html', lform=lform, rform=rform, error = error)

@app.route('/login', methods=['POST'])
def login():
	global login_errors
	lform = LoginForm()
	rform = RegisterForm()
	login_errors = validate_login(lform)
	if login_errors == None:
		return redirect(url_for('home'))
	else:
		return redirect(url_for('index'))
		
		

@app.route('/register')
def register():
	global register_errors
	error = register_errors
	lform = LoginForm()
	rform = RegisterForm()
	register_errors = validate_register(rform)
	if register_errors == None:
		return redirect(url_for('home'))
	else:
		return redirect(url_for('index'))


@app.route('/_logout')
def logout():
	pass

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
