import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.forms import GifForm
from app.models import Gif

@app.route('/')
@app.route('/index')
def index():
    gifs = Gif.query.all()
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
        path = os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        )
        f.save(path)
        gif = Gif(name=filename, path=path, filesize=os.path.getsize(path))
        db.session.add(gif)
        db.session.commit()
        flash('Added {} to your frame!'.format(filename))

        return redirect(url_for('index'))
    elif request.method == 'POST':
        print(form.errors)
        error = form.errors['gif'][0]


    return render_template('upload.html', form=form, error=error)

@app.route('/delete/<gif_id>', methods=['POST'])
def delete_gif(gif_id):
    gif = Gif.query.get(int(gif_id))
    if gif :
        if os.path.exists(gif.path):
            os.remove(gif.path)
        db.session.delete(gif)
        db.session.commit()
        flash('Removed {} from your frame!'.format(gif.name))
    return redirect(url_for('index'))
