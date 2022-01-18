from flaskapp import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture_url = db.Column(db.String(140))
    posted_at = db.Column(db.DateTime)
    parsed_at = db.Column(db.DateTime)
