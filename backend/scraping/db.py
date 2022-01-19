from typing import Dict

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class DBConnect:
    def __init__(self, db_url: str):
        """prepare and automap db"""

        self._Base = automap_base()
        self._engine = create_engine(db_url)
        self._Base.prepare(self._engine, reflect=True)

        self.News = self._Base.classes.news

    def __enter__(self):
        self.session = Session(self._engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def add_news(self, news: list[Dict]):
        for one_news in news:
            self.session.merge(self.News(title=one_news['title'],
                                         picture_url=one_news['picture_url'],
                                         posted_at=one_news['posted_at'],
                                         parsed_at=one_news['parsed_at'],
                                         text=one_news['text']))
        self.session.commit()
