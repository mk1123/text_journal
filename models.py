
from sqlalchemy.dialects.postgresql import JSON
from app import db


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String)
    date = db.Column(db.DateTime, unique=True)
    text = db.Column(db.String)

    def __init__(self, phone_num, date, text):
        self.phone_num = phone_num
        self.date = date
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)
