from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PushupForm(FlaskForm):
    pushup_count = IntegerField('Number of pushups', default=10, validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Submit')