from flaskapp import db


class News(db.Model):
    title = db.Column(db.String(140), primary_key=True)
    picture_url = db.Column(db.String(140), primary_key=True)
    posted_at = db.Column(db.DateTime, primary_key=True)
    parsed_at = db.Column(db.DateTime)
    text = db.Column(db.Text)
