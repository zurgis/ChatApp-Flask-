from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path) # Загружаем все переменные, найденные, как переменные среды

class Config:
    """ Устанавливает конфигурации Flask из файла .env """
    # Получаем значения переменных
    TESTING = os.getenv('TESTING')
    FLASK_DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')