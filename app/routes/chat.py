from flask import Blueprint, render_template, redirect, url_for, session
from flask_socketio import join_room, leave_room, send
from app.models.forms import LoginForm
from app.utils.config import socketio

chat = Blueprint('chat', __name__)

rooms = {}


@chat.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
        session['room'], session['user'] = form.room.data, form.user.data
        return redirect(url_for('chat.room'))
    return render_template('index.html', form=form)


@chat.route('/room')
def room():
    room, user = session.get('room'), session.get('user')
    return render_template('room.html', room=room, user=user)


@socketio.event
def join(data):
    room, user = data['room'], data['user']
    if room not in rooms:
        rooms[room] = {
            'connected': 1,
            'members': [user, ]
        }
    elif user not in rooms[room]['members']:
        rooms[room]['connected'] += 1
        rooms[room]['members'].append(user)
    join_room(room)
    send({'user': user, 'msg': 'entro a la sala'}, to=room)
    send({
        'members': rooms[room]['members'],
        'connected': rooms[room]['connected']
    }, to=room)


@socketio.event
def disconnect():
    room, user = session.get('room'), session.get('user')
    if user in rooms[room]['members']:
        rooms[room]['connected'] -= 1
        rooms[room]['members'].remove(user)
    leave_room(room)
    session.clear()
    send({'user': user, 'msg': 'dejo la sala'}, to=room)
    send({
        'members': rooms[room]['members'],
        'connected': rooms[room]['connected']
    }, to=room)


@socketio.event
def message(data):
    send({'user': data['user'], 'msg': data['msg']}, to=data['room'])
