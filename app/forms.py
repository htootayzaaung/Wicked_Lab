from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from .models import User

#Log-in form to ask users to log in 
class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Log In')

#Change-password form to ask users to change and update passsword!
class CpasswordForm(FlaskForm):
    password = PasswordField('Password: ', validators=[DataRequired()])
    npassword = PasswordField('Enter New Password: ', validators=[DataRequired()])
    renpassword = PasswordField('Re-Enter New Paswod: ', validators=[DataRequired(), EqualTo('npassword')])
    submit = SubmitField('Change Password')

#Registration form to ask users to create an account!
class RegistrationForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(),Email()])
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password: ', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')
