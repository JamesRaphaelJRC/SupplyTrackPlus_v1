#!/usr/bin/python3
''' Defines the User class'''
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_flask import db
from models.base_model import BaseModel
from web_flask import login


class User(BaseModel, UserMixin, db.Model):
    ''' Define table for User instances '''
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    username =  db.Column(db.String(65), index=True, unique=True,
                          nullable=False)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(20))
    vendors = db.relationship('Vendor', backref='user',
                              cascade='all, delete-orphan', lazy=True)
    orders = db.relationship('Order', backref='user',
                             cascade='all, delete-orphan', lazy=True)
    reviews = db.relationship('Review', backref='review',
                              cascade='all, delete-orphan', lazy=True)


    def set_password(self, password):
            ''' Sets the user password to a hash_password '''
            self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        ''' Verifies a user password if correct'''
        return check_password_hash(self.password_hash, password)


    @login.user_loader
    def load_user(id):
         return User.query.get(id)
    
