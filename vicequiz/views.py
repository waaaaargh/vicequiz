from random import randint

from flask import request, render_template, jsonify

from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound

from vicequiz import app, db
from vicequiz.models import Tweet

@app.route('/')
def welcome_view():
    return render_template('index.html')
    
@app.route('/backend/get_random_tweet')
def get_random_tweet():
    # determine number of tweets available
    number_of_tweets = Tweet.query.count()

    # get random tweet
    offset = randint(0,number_of_tweets)
    random_tweet = Tweet.query.offset(offset).limit(1).one()

    return jsonify({
        'id': random_tweet.id,
        'text': random_tweet.text
    })
    
@app.route('/backend/answer/<int:tweet_id>')
def answer(tweet_id):
    tweet = Tweet.query.filter(tweet_id == Tweet.id).first()
    if tweet is None:
        return jsonify({
            'error': 'No such tweet :('
        }), 404

    answer = request.args['answer']
    if answer not in app.config['TWITTER_ACCOUNT_NAMES']:
        return jsonify({
            'error': 'Sorry, invalid answer.'
        }), 401
        
    return jsonify({
        'result': answer == tweet.screenname,
        'tweet': {
            'text': tweet.text,
            'id': tweet.tweet_id,
            'account_name': tweet.screenname
        }
    })
