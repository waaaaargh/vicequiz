#!/usr/bin/env python
import sys
from argparse import ArgumentParser

if __name__ == "__main__":
    aparser = ArgumentParser(description="vicequiz")
    
    aparser.add_argument("command", help="command to run")
    
    args = aparser.parse_args()

    if args.command == 'runserver':
        from vicequiz import app
        app.run(debug=True)
    elif args.command == 'initdb':
        from vicequiz import db
        db.create_all()
    elif args.command == 'filldb':
        from vicequiz import app, db
        from vicequiz.models import Tweet
        from twython import Twython
        
        twitter = Twython(app.config['TWITTER_APP_KEY'],
                          app.config['TWITTER_APP_SECRET'],
                          app.config['TWITTER_OAUTH_TOKEN'],
                          app.config['TWITTER_OAUTH_SECRET'])
        
        import re
        rt_matcher = re.compile(r"RT \@.*:\ ")
        url_matcher = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        
        sess = db.session()

        for account_name in app.config['TWITTER_ACCOUNT_NAMES']:
            for tweet in twitter.get_user_timeline(screen_name=account_name,
                                                   count=100):
                text = tweet['text']
                text = rt_matcher.sub('', text)
                text = url_matcher.sub('', text)

                t = Tweet()
                t.text = text.strip()
                t.tweet_id = tweet['id_str']
                t.screenname = tweet['user']['screen_name']
                
                if len(t.text) > 10:
                    sess.add(t)

        sess.commit()
        
        
    else:
        print("[i] command not found, exitting")
        sys.exit(-1)
