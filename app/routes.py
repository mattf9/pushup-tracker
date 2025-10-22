from flask import flash, redirect, render_template, url_for
from app import app
from datetime import datetime
from app.forms import LoginForm, PushupForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Joe'}

    pushup_sets = [
        {
            'username': 'Joe',
            'pushup_count': 15,
            'pushup_time': "2025-10-19 08:16:57"
        },
        {
            'username': 'Joe',
            'pushup_count': 20,
            'pushup_time': "2025-10-19 08:16:57"
        }
    ]
    form = PushupForm()
    return render_template('index.html', title='Home', user=user, pushup_sets=pushup_sets, form=form)
    # return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)