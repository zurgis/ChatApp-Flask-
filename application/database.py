import sqlite3
from sqlite3 import Error
from datetime import datetime

FILE = 'messages.db'
PLAYLIST_TABLE = 'Messages'

class DataBase:
    """ Используется для подключения, чтения и записи """
    def __init__(self):
        """ Подключение к файлу БД """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()
    
    def close(self):
        """ Закрываем подключение """
        self.conn.close()

    def _create_table(self):
        """ Создаем новую таблицу, если она не существует """
        query = f'''CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)'''
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100, name=None):
        """ Возвращает все сообщения """
        if not name:
            query = f'SELECT * FROM {PLAYLIST_TABLE}'
            self.cursor.execute(query)
        else:
            query = f'SELECT * FROM {PLAYLIST_TABLE} WHERE name = ?'
            self.cursor.execute(query, (name,))

        result = self.cursor.fetchall()

        # Возвращает сообщения отсортированные по дате
        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {'name': name, 'message': content, 'time': str(date)}
            results.append(data)

        return list(reversed(results))

    def get_messages_by_name(self, name, limit=100):
        """ Получить список сообщений по имени """
        return self.get_all_messages(limit, name)

    def save_message(self, name, msg):
        """ Сохраняет сообщение в таблицу """
        query = f'INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)'
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()