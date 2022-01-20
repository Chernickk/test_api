import datetime

from flask import request

from flaskapp import app
from flaskapp.models import News


@app.route('/news')
def get_news():
    day = request.args.get('day', default=0, type=int)
    hour = request.args.get('hour', default=0, type=int)

    if day or hour:
        date_time = datetime.datetime.now() - datetime.timedelta(days=day, hours=hour)
        news = News.query.filter(News.posted_at >= date_time).all()
    else:
        news = News.query.all()

    news = [{'title': row.title,
             'picture_url': row.picture_url,
             'posted_at': row.posted_at,
             'text': row.text} for row in news]

    return {'news': news}
