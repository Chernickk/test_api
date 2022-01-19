import asyncio
from multiprocessing import Process
from datetime import datetime
from time import sleep
from typing import Dict

import aiohttp
import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from config import Config

URL = 'https://mosmetro.ru'
MAIN_PAGE = f'{URL}/news/'


class Parser:
    def __init__(self, base_url: str, path: str):
        self.base_url = base_url
        self.path = path
        self.date_dict = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12',
        }

    def get_date_from_string(self, date: str) -> datetime:
        month_word = date.split()[1][:-1]
        month_num = self.date_dict[month_word]
        date = date.replace(month_word, month_num)
        date = datetime.strptime(date, '%d %m, %H:%M')
        date = date.replace(year=datetime.now().year)

        return date

    def get_news_data(self, page: str) -> Dict:
        soup = BeautifulSoup(page, 'html.parser')

        picture_url = soup.find('img', class_='article__image')['src']
        title = soup.find('p', class_='article__title').text
        date = soup.find('p', class_='article__date').text
        posted_at = self.get_date_from_string(date)

        article_block = soup.findAll('div', {'class': 'article__block'})
        text = ' '.join([p.text for p in article_block])

        return {
            'picture_url': picture_url,
            'title': title,
            'posted_at': posted_at,
            'text': text,
            'parsed_at': datetime.now()

        }

    def get_news_urls(self, news: list) -> list:
        urls_list = [a.get('href') for a in news]

        return urls_list

    async def get_news_page(self, session: aiohttp.ClientSession, url: str) -> str:
        page = await session.get(url)
        text = await page.text()
        return text

    async def get_news_pages(self) -> tuple:
        page = requests.get(MAIN_PAGE)
        soup = BeautifulSoup(page.text, "html.parser")

        news = soup.findAll('a', {'class': 'news-card'})
        urls = self.get_news_urls(news)

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.get_news_page(session, f'{self.base_url}{url}')) for url in urls]
            pages = await asyncio.gather(*tasks)

        return pages

    def parse(self):
        pages = asyncio.run(self.get_news_pages())

        news = []

        for page in pages:
            news.append(self.get_news_data(page))

        return news


class DBConnect:
    def __init__(self, db_url):
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


class Worker(Process):
    def __init__(self, db_url, base_url, path):
        super().__init__()
        self.connection = DBConnect(db_url=db_url)
        self.parser = Parser(base_url=base_url, path=path)

    def run(self) -> None:
        while True:
            news = self.parser.parse()
            with self.connection as conn:
                conn.add_news(news)
            sleep(15 * 60)


if __name__ == '__main__':
    print(Config.SQLALCHEMY_DATABASE_URI)
    w = Worker(Config.SQLALCHEMY_DATABASE_URI, URL, MAIN_PAGE)
    w.start()
