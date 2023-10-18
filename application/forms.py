from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    BooleanField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
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

class EditProfileForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired()]
    )
    about_me = TextAreaField(
        label='About me',
        validators=[Length(min=0, max=140)]
    )
    submit = SubmitField(
        label='Submit'
    )

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EmptyForm(FlaskForm):
    submit = SubmitField(
        label='Submit'
    )

class PostForm(FlaskForm):
    post = TextAreaField(
        label='Say somthing',
        validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(
        label='Submit'
    )