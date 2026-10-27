from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.models import User, Pushup
from datetime import datetime, timedelta, timezone
from app.forms import LoginForm, PushupForm
from sqlalchemy import func, desc, select
from zoneinfo import ZoneInfo

@app.route('/')
@app.route('/index')
def index():
    all_time_reps, all_time_sets = get_stats_all_users()

    # set default number of pushups to users average
    if current_user.is_authenticated:
        try:
            query = db.select(func.floor(func.avg(Pushup.reps))).where(Pushup.user_id == current_user.id)
            result = db.session.execute(query)
            pushup_average = result.scalars().one()
        except:
            pushup_average = 15
    else:
        pushup_average = 10
    pushup_sets = db.session.execute(db.select(Pushup).order_by(Pushup.timestamp.desc())).scalars()
    timezone = ZoneInfo('America/New_York')
    seven_days_ago = datetime.now(timezone) - timedelta(days=7)
    last_7_day_sets = db.session.query(User.username, func.count(Pushup.id).label('set_count')).select_from(User).join(Pushup).group_by(User.username).where(Pushup.timestamp >= seven_days_ago).order_by(desc('set_count'))

    this_month = datetime.utcnow() - timedelta(days=30)

    sets_this_month = db.session.query(
        func.count(Pushup.id)
        ).where(
        Pushup.timestamp >= this_month).scalar()

    last_month = datetime.utcnow() - timedelta(days=60)

    sets_last_month = db.session.query(
        func.count(Pushup.id)
            ).where(Pushup.timestamp.between(last_month, this_month)).scalar()

    form = PushupForm()
    return render_template('index.html', title='Home', pushup_sets=pushup_sets, pushup_average=pushup_average, 
                           last_7_day_sets=last_7_day_sets, all_time_reps=all_time_reps, all_time_sets=all_time_sets, 
                           sets_this_month=sets_this_month, sets_last_month=sets_last_month, form=form)



@app.route('/log_set', methods=['POST'])
@login_required
def log_set():
    pushup = Pushup(user_id = current_user.id, timestamp = datetime.now(), reps = request.form['pushup_count'])
    db.session.add(pushup)
    db.session.commit()
    flash('pushup set logged!')
    return redirect(url_for('user', username=current_user.username))

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

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username ==  username)) 
    
    query = select(func.count(Pushup.id).label('set_count')).where(Pushup.user_id == user.id)
    all_time_sets = db.session.execute(query).scalar_one()
    if not all_time_sets:
        print("no sets")
        all_time_reps = 0
        all_time_sets = 0
        max_reps = {"reps": 0, "timestamp": ""}
    else:
        query = select(func.sum(Pushup.reps).filter(Pushup.user_id == user.id))
        all_time_reps = db.session.execute(query).scalar_one()

        query = select(Pushup).where(Pushup.user_id == user.id).order_by(desc(Pushup.reps)).limit(1)
        max_reps = db.session.execute(query).scalar_one_or_none()

        this_month = datetime.utcnow() - timedelta(days=30)
        query = select(func.count(Pushup.id).label('set_count')).where(Pushup.user_id == user.id).where(Pushup.timestamp >= this_month)
        sets_this_month = db.session.execute(query).scalar_one_or_none()

        last_month = datetime.utcnow() - timedelta(days=60)
        query = select(func.count(Pushup.id).label('set_count')).where(Pushup.user_id == user.id).where(Pushup.timestamp.between(last_month, this_month))
        sets_last_month = db.session.execute(query).scalar_one_or_none()

    return render_template('user.html', user=user, all_time_sets=all_time_sets, all_time_reps=all_time_reps, 
                           max_reps=max_reps, sets_this_month=sets_this_month, sets_last_month=sets_last_month)

def get_stats_all_users():
    all_time_reps = db.session.query(
        func.sum(Pushup.reps)
    ).scalar()

    all_time_sets = db.session.query(
        func.count()
    ).select_from(Pushup).scalar()

    all_time_reps = all_time_reps or 0

    return all_time_reps, all_time_sets