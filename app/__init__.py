from flask import Flask
import os
try:
    from .APIKEYS import *
    os.environ["ALCHEMY_KEY"] =  ALCHEMY_KEY
    os.environ["YOUTUBE_CLIENT_ID"] = YOUTUBE_CLIENT_ID
    os.environ["YOUTUBE_CLIENT_SECRET"] = YOUTUBE_CLIENT_SECRET
    os.environ["REDIRECT_URI"] = REDIRECT_URI
    os.environ["DEVELOPER_KEY"] = DEVELOPER_KEY
    os.environ["TWEEPY_ACCESS_TOKEN"] = TWEEPY_ACCESS_TOKEN
    os.environ["TWEEPY_ACCESS_TOKEN_SECRET"] = TWEEPY_ACCESS_TOKEN_SECRET
    os.environ["TWEEPY_CONSUMER_KEY"] = TWEEPY_CONSUMER_KEY
    os.environ["TWEEPY_CONSUMER_SECRET"] = TWEEPY_CONSUMER_SECRET
except Exception as e:
    print "Error: Couldn't find APIKEYS.py please provide yours"
    print e

app = Flask(__name__)
app.config.from_object('config')
#app.config.from_pyfile('APIKEYS.py')

from app import views