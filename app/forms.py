from flask_wtf import FlaskForm
from wtforms import IntegerField, IntegerRangeField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PushupForm(FlaskForm):
    pushup_count = IntegerField('Number of pushups', default=10, validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Submit')