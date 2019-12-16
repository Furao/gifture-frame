from flask_wtf import FlaskForm
from wtforms import DecimalField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.recaptcha.validators import ValidationError
from app.models import Gif

class GifForm(FlaskForm):
    gif = FileField(validators=[
        FileRequired(),
        FileAllowed(['gif'], 'Gifs only!')
    ])

    def validate_gif(self, gif):
        g = Gif.query.filter_by(name=gif.data.filename).first()
        if g is not None:
           raise ValidationError('File with this name already exists.')

class SettingsForm(FlaskForm):
    play_length = DecimalField('Gif Play Length')
    shuffle = BooleanField('Shuffle')
    submit = SubmitField('Apply')
