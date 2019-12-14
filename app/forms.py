from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class GifForm(FlaskForm):
    gif = FileField(validators=[
        FileRequired(),
        FileAllowed(['gif'], 'Gifs only!')
    ])