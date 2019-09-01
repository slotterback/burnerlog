from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id            = db.Column( db.Integer    , primary_key=True )
    username      = db.Column( db.String(64) , index=True, unique=True )
    email         = db.Column( db.String(120), index=True, unique=True )
    password_hash = db.Column( db.String(128) )
    reports =  db.relationship('Report', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Customer(db.Model):
    id = db.Column( db.Integer, primary_key=True )
    customer_name = db.Column( db.String(128), index=True, unique=True )
    customer_notes = db.Column( db.String(2048) )
    reports = db.relationship('Report', backref='customer', lazy='dynamic')


class Report(db.Model):
    id = db.Column( db.Integer, primary_key=True )
    user_id = db.Column( db.Integer, db.ForeignKey('user.id') )
    customer_id = db.Column( db.Integer, db.ForeignKey('customer.id') )
    timestamp = db.Column( db.DateTime, index=True, default=datetime.utcnow )
    summary = db.Column( db.String(1024), index=True )
    action = db.Column( db.String(30000) )
    recommendation = db.Column( db.String(2048) )
    
    def __repr__(self):
        return '<Report {}>'.format(self.summary)


