import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("POSTGRES_USER")}:' \
                              f'{os.environ.get("POSTGRES_PASSWORD")}@db:5432/' \
                              f'{os.environ.get("POSTGRES_DB")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = 'https://mosmetro.ru'
    PATH = '/news/'
