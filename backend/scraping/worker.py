import asyncio
from multiprocessing import Process
from datetime import datetime
from time import sleep
from typing import Dict

import aiohttp
import requests
from bs4 import BeautifulSoup

from scraping.db import DBConnect


class Scraper:
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

        # avoid mistakes at beginning of the year
        if date.month == 12 and datetime.now().month == 1:
            date = date.replace(year=datetime.now().year - 1)
        else:
            date = date.replace(year=datetime.now().year)

        return date

    def find_news_data(self, page: str) -> Dict:
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

    async def find_news_pages(self) -> tuple:
        page = requests.get(f'{self.base_url}{self.path}')
        soup = BeautifulSoup(page.text, "html.parser")

        news = soup.findAll('a', {'class': 'news-card'})
        urls = self.get_news_urls(news)

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.get_news_page(session, f'{self.base_url}{url}')) for url in urls]
            pages = await asyncio.gather(*tasks)

        return pages

    def scrape(self) -> list:
        pages = asyncio.run(self.find_news_pages())

        news = []

        for page in pages:
            news.append(self.find_news_data(page))

        return news


class Worker(Process):
    def __init__(self, db_url: str, base_url: str, path: str):
        super().__init__()
        self.connection = DBConnect(db_url=db_url)
        self.scraper = Scraper(base_url=base_url, path=path)

    def run(self) -> None:
        while True:
            try:
                news = self.scraper.scrape()
                with self.connection as conn:
                    conn.add_news(news)
                sleep(10 * 60)
            except Exception as e:
                print(f'Scraping job failed: {e}')
