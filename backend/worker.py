from scraping.worker import Worker
from config import Config

if __name__ == '__main__':
    w = Worker(Config.SQLALCHEMY_DATABASE_URI, Config.BASE_URL, Config.PATH)
    w.start()
