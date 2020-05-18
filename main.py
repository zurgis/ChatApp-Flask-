from flask_socketio import SocketIO

from application import create_app
from application.database import DataBase
import config

# SETUP
app = create_app()
socketio = SocketIO(app) # Используется для общения с пользователем

@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """ Обрабатывает сохранение полученных с веб-сервера сообщений
        и отправляет сообщения другим клиентам
    """
    data = dict(json)
    if 'name' in data:
        db = DataBase()
        db.save_message(data['name'], data['message'])

    socketio.emit('message response', json) # Отправляем клиенту

# MAINLINE
if __name__ == '__main__': # Запускает веб-сервер
    socketio.run(app, debug=True, host=str(config.Config.SERVER))