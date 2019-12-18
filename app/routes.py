import os
from app import app, db, animate_server, animator
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.forms import GifForm, SettingsForm, ControlsForm
from app.models import Gif, Settings

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ControlsForm()
    gifs = Gif.query.order_by(Gif.name).all()
    if form.validate_on_submit():
        if form.play.data:
            print("Play")
            s = Settings.query.get(1)
            res = animator.play_gifs([gif.path for gif in gifs], s.play_length)
        elif form.stop.data:
            print("Stop")
            res = animator.stop_gifs()
    return render_template('index.html', gifs=gifs, form=form)

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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    s = Settings.query.get(1)
    if request.method == 'GET':
        if not s:
            s = Settings(play_length=30.0, shuffle=True)
            db.session.add(s)
            db.session.commit()
        form.play_length.data = s.play_length
        form.shuffle.data = s.shuffle
    if form.validate_on_submit():
        s.play_length = abs(form.play_length.data)
        s.shuffle = form.shuffle.data
        db.session.commit()
        return redirect(url_for('settings'))

    return render_template('settings.html', form=form)