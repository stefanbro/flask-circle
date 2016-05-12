from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, IntegerField, validators


class LoginForm(Form):
	email = StringField('email', [validators.DataRequired(), validators.Email()])
	password = PasswordField('password', [validators.DataRequired()])
	
class RegisterForm(Form):
	first_name = StringField('name', [validators.DataRequired()])
	email = StringField('email', [validators.DataRequired()])
	password = PasswordField('password', [validators.DataRequired()])
	password_again = PasswordField('password_again')
	
class SettingsForm(Form):
	time = IntegerField('time', [validators.DataRequired()])
	short_break = IntegerField('short_break', [validators.DataRequired()])
	long_break = IntegerField('long_break', [validators.DataRequired()])
	before_long_break = IntegerField('before_long_break', [validators.DataRequired()])