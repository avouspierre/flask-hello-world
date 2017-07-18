import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager(app)
lm.login_view = 'login'
oauth =  OAuth()

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key= app.config['TWITTER_CONSUMER_KEY'],
                           consumer_secret=app.config['TWITTER_CONSUMER_SECRET']
)

from app import views, models
