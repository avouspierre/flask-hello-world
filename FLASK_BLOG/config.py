import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Une-super-cle-introuvable'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

TWITTER_CONSUMER_KEY = 'To updated'
TWITTER_CONSUMER_SECRET = 'To updated'
