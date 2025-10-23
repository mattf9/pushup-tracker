from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.models import User, Pushup
from datetime import datetime
from app.forms import LoginForm, PushupForm

@app.route('/')
@app.route('/index')
def index():

    # pushup_sets = Pushup.query.all()
    pushup_sets = db.session.execute(db.select(Pushup).order_by(Pushup.timestamp.desc())).scalars()
    form = PushupForm()
    return render_template('index.html', title='Home', pushup_sets=pushup_sets, form=form)
    # return render_template('index2.html', title='Home', form=form)
    # return render_template('index.html')


@app.route('/log_set', methods=['POST'])
@login_required
def log_set():
    pushup = Pushup(user_id = current_user.id, timestamp = datetime.now(), body = request.form['pushup_count'])
    db.session.add(pushup)
    db.session.commit()
    flash('pushup set logged!')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
        
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))