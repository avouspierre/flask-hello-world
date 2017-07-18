"""
    set of routes of the app
"""

from app import app, lm, db, twitter
from flask import render_template, flash, redirect, g, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from .models import User



@app.before_request
def before_request():
    """before each request"""
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@app.route('/')
@app.route('/index')
@login_required
def index():
    """display the home page"""
    user = g.user
    posts = [
        {
            'author':{'nickname':'Pierre'},
            'body':'Beautiful day in Leucate'
        },
        {
            'author':{'nickname':'Anaelle'},
            'body':'I love the sea'
        },
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ route to Twitter authentication """
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    return twitter.authorize(callback=url_for('oauth_authorized',
                                              next=request.args.get('next')
                                              or request.referrer or None))

@app.route('/oauth_authorized')
def oauth_authorized():
    """ callback after login by twitter"""
    next_url = request.args.get('next') or url_for('index')
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in')
        return redirect(next_url)

    session['twitter_oauth'] = resp
    flash('You were signed in as %s' % resp['screen_name'])

    user = User.query.filter_by(social_id=resp['user_id']).first()
    if user is None:
        nickname = resp['screen_name']
        user = User(nickname=nickname, social_id=resp['user_id'])
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=False)
    return redirect(next_url)

@twitter.tokengetter
def get_twitter_token(token=None):
    """function required by oauth"""
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.route('/logout')
def logout():
    """ route to logout"""
    logout_user()
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))

@lm.user_loader
def load_user(identifier):
    """route required by flask_login
    :type identifier: String
    """
    return User.query.get(int(identifier))
