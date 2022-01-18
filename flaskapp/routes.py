import datetime

from flaskapp import app
from flask import request
from flaskapp.models import News


@app.route('/news')
def news():
    day = request.args.get('day')
    news = None
    if day:
        dt = datetime.datetime.now() - datetime.timedelta(days=int(day))
        news = News.query.filter(News.posted_at >= dt).all()

    return {
        'status': 'ok',
        'news': news
    }