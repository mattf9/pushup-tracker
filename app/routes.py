from flask import render_template
from app import app
from datetime import datetime
from app.forms import PushupForm

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