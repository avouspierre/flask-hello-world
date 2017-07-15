from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'Anaelle'}
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
