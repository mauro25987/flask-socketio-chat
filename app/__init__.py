from flask import Flask
from app.utils.config import socketio
from app.routes.chat import chat as chat_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    socketio.init_app(app)

    app.register_blueprint(chat_blueprint)

    return app
