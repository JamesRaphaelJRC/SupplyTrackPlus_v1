#!/usr/bin/python3
''' The Basemodel class '''
from uuid import uuid4
from datetime import datetime
from web_flask import db

class BaseModel():
    ''' Defines the BaseModel class'''
    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        ''' Instantiation of a new BaseModel object'''
        self.id = str(uuid4())
        self.created_at = datetime.now()

        if kwargs:
            try:
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at'])
                del kwargs['__class__']
            except Exception:
                pass
            self.__dict__.update(kwargs)

    def __str__(self):
        ''' Returns a string representation of BaseModel instance'''
        class_name = type(self).__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def to_dict(self):
        ''' Converts an object to a dictionary '''
        dictionary = self.__dict__.copy()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary
