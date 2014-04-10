from vicequiz import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String)
    text = db.Column(db.String)
    screenname = db.Column(db.String)
