from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, Length

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired(), Length(4, 64),
                                                     Regexp('^[A-Za-z][A-za-z0-9_.]*$', 0, 'Invalid username')])
    email = StringField('Email Address:', validators=[DataRequired(), Length(1, 64),
                                                      Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8, 64),
                                                      EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.select(User.email).where(User.email == field.data).exists():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.select(User.username).where(User.username == field.data).exists():
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email Address:', validators=[DataRequired(),
                                                      Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[DataRequired(), Length(8, 64)])
    new_password2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                  EqualTo(
                                                                      'new_password', message='Password must match')])
    submit = SubmitField('Submit')
