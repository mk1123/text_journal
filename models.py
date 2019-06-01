
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime, unique=True)
    text = db.Column(db.String)

    def __init__(self, name, date, text):
        self.name = name
        self.date = date
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String)
    name = db.Column(db.String)
    username = db.Column(db.String)
    authenticated = db.Column(db.Boolean)
    password_hash = db.Column(db.String)
    
    def __init__(self, phone_num, name):
        self.phone_num = phone_num
        self.name = name
        self.username = name.lower().replace(' ', '_')
        self.authenticated = False
        
    def is_authenticated(self):
        return self.authenticated
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return self.username
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
    
