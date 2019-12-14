import os
from app import app
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.forms import GifForm

@app.route('/')
@app.route('/index')
def index():
    gifs = [
        {'name': 'converse.gif', 'tags': ['animated', 'shoes']},
        {'name': 'dance.gif', 'tags': ['live', 'cute']},
    ]
    return render_template('index.html', gifs=gifs)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    error = None
    form = GifForm()
    if form.validate_on_submit():
        f = form.gif.data
        filename = secure_filename(f.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        return redirect(url_for('index'))
    elif request.method == 'POST':
        error = "Must select .gif file"

    return render_template('upload.html', form=form, error=error)