from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint

from .database import DataBase

view = Blueprint('views', __name__)

# GLOBAL CONSTANTS
NAME_KEY = 'name'
MSG_LIMIT = 20

@view.route('/login', methods=['POST', 'GET'])
def login():
    """ Показывает страницу логина """
    if request.method == 'POST':
        name = request.form['inputName']
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f'You were successfully logged in as {name}.') # Всплывающее сообщение
            return redirect(url_for('views.home'))
        else:
            flash('1Name must be longer than 1 character')
    
    return render_template('login.html', **{'session': session})

@view.route('/logout')
def logout():
    """ Выход из сеанса """
    session.pop(NAME_KEY, None)
    flash('0You were logged out')
    return redirect(url_for('views.login'))

@view.route('/')
@view.route('/home')
def home():
    """ Отображает домашнюю страницу, если залогинен """
    if NAME_KEY not in session:
        return redirect(url_for('views.login'))

    return render_template('index.html', **{'session': session})

@view.route('/history')
def history():
    if NAME_KEY not in session:
        flash('0Please login before viewing message history')
        return redirect(url_for('views.login'))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template('history.html', **{'history': json_messages})

@view.route('/get_name')
def get_name():
    data = {'name': ''}
    if NAME_KEY in session:
        data = {'name': session[NAME_KEY]}
    return jsonify(data) # Превращаем вывод json в объект response

@view.route('/get_messages')
def get_messages():
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)
    
    return jsonify(messages)

@view.route('/get_history')
def get_history(name):
    db = DataBase()
    msgs = db.get_messages_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages

# UTILITIES
def remove_seconds_from_messages(msgs):
    """ Удаляет секунды из всех сообщений """
    messages = []
    for msg in msgs:
        message = msg
        message['time'] = remove_seconds(message['time'])
        messages.append(message)

    return messages

def remove_seconds(msg):
    return msg.split('.')[0][:-3]