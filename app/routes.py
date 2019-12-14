from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    gifs = [
        {'name': 'converse.gif', 'tags': ['animated', 'shoes']},
        {'name': 'dance.gif', 'tags': ['live', 'cute']},
    ]
    return render_template('index.html', gifs=gifs)
