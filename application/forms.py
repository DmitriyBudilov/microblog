from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, Email

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