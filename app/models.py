from app import db
from datetime import datetime

class Gif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    path = db.Column(db.String(120), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    filesize = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Gif {}>'.format(self.name)
