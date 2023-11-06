#!/usr/bin/python3
''' Defines the Review class '''
from sqlalchemy.ext.hybrid import hybrid_property
from web_flask import db
from models.base_model import BaseModel


class Review(BaseModel, db.Model):
    ''' Define table for Review instances '''
    content = db.Column(db.String(255))
    order_id = db.Column(db.String(60), db.ForeignKey('order.id'))
    vendor_id = db.Column(db.String(60), db.ForeignKey('vendor.id'))
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, nullable=False, default=0)

    @hybrid_property
    def vendor_name(self):
        ''' Retrieves and returns the vendor's name associated with an
            order to be reviewed
        '''
        from models import storage
        return storage.get('Vendor', self.vendor_id).name
    
    @hybrid_property
    def product_name(self):
        ''' Retrieves and returns the product name to be reviewed '''
        from models import storage
        return storage.get('Order', self.order_id).product_name
