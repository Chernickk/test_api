from datetime import datetime

from bs4 import BeautifulSoup
import requests

URL = 'https://mosmetro.ru'
MAIN_PAGE = f'{URL}/news/'


class Parser:
    def __init__(self, url, main_page):
        self.url = url
        self.main_page = main_page
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

    def get_image_caption_date(self, a):
        image_style = a.findNext('div', {'class': "news-card__image"}).get('style')
        image_url = image_style.split('(')[1].split(')')[0]

        caption = a.findNext('div', {'class': "news-card__caption"}).text

        date = a.findNext('div', {'class': "news-card__date"}).text
        month_word = date.split()[1][:-1]
        month_num = self.date_dict[month_word]
        date = date.replace(month_word, month_num)
        date = datetime.strptime(date, '%d %m, %H:%M')
        date = date.replace(year=datetime.now().year)

        path = a.get('href')

        return image_url, caption, date, path

    def get_news_text(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        article_block = soup.findAll('div', {'class': 'article__block'})

        text = ' '.join([p.text for p in article_block])
        return text

    def get_news(self, news):
        news_list = []
        for a in news:
            image_url, caption, date, path = self.get_image_caption_date(a)
            news_url = f'{self.url}{path}'
            text = self.get_news_text(news_url)

            news_list.append({
                'image_url': image_url,
                'caption': caption,
                'date': date,
                'text': text
            })

        return news_list

    def parse(self):
        page = requests.get(MAIN_PAGE)
        soup = BeautifulSoup(page.text, "html.parser")

        news = soup.findAll('a', {'class': 'news-card'})

        return self.get_news(news)


p = Parser(URL, MAIN_PAGE)
news = p.parse()
print(news)
