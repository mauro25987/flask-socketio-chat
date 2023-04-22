from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    user = StringField('user', validators=[InputRequired()])
    room = StringField('room', validators=[InputRequired()])
    send = SubmitField('join')
