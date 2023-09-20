from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from application import app
from .forms import LoginForm

@app.route('/')
@app.route('/index/')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.jinja2', title='Home', posts=posts, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.jinja2', title='Sign In', form=form)