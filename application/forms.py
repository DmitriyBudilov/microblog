from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    ValidationError,
    EqualTo
)

from application.models import User

class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            DataRequired(message='Введите имя пользователя!')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(message='Введите пароль пользователя!')
        ]
    )
    remember_me = BooleanField(
        label='Remember Me'
    )
    submit = SubmitField(
        label='Sign In'
    )

class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            DataRequired(message='Enter username!')
        ]
    )
    email = EmailField(
        label='Email',
        validators=[
            DataRequired(message='Enter email!'),
            Email(message='With str is not email!')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(message='Enter password!')
        ]
    )
    password2 = PasswordField(
        label='Repeat Password',
        validators=[
            DataRequired(message='Enter password'),
            EqualTo(fieldname='password', message='Not equal to password!')
        ]
    )
    submit = SubmitField(
        label='Register'
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
