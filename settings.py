import os
from pathlib import Path
from dotenv import load_dotenv

from db import load_db


def load_settings(env):
    env_path = Path('settings') / '.env.{}'.format(env)
    load_dotenv(dotenv_path=env_path)


def get_db_settings():
    return {
        'port': int(os.getenv('DB_PORT')),
        'host': os.getenv('DB_HOST'),
        'name': os.getenv('DB_NAME')
    }


def get_app_settings():
    return {
        'autoreload': bool(os.getenv('AUTORELOAD')),
        'debug': bool(os.getenv('DEBUG')),
        'serve_traceback': bool(os.getenv('SERVE_TRACEBACK')),
        'db': load_db(get_db_settings())
    }