from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    user = StringField('User', validators=[InputRequired()])
    room = StringField('Room', validators=[InputRequired()])
    send = SubmitField('Join')
