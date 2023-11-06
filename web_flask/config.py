#!/usr/bin/python3
''' Defines the Flask-SQLAlchemy configuration with environmental variables '''
import os
from dotenv import load_dotenv

# Loads the .env file
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ''' Handles all environmental variables configurations '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
