#!/usr/bin/python3
''' Defines the Order class'''
from sqlalchemy.ext.hybrid import hybrid_property
from web_flask import db
from models.base_model import BaseModel


class Order(BaseModel, db.Model):
    ''' Define table for Order instances '''
    product_name = db.Column(db.String(60), index=True, nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20))
    unit_cost = db.Column(db.Integer)
    delivery_status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    vendor_id = db.Column(db.String(60), db.ForeignKey('vendor.id'))
    reviews = db.relationship('Review', backref='order', uselist=True,
                              cascade='all, delete-orphan', lazy=True)

    @hybrid_property
    def vendor_name(self):
        ''' Returns the name of the vendor related to an order '''
        from models import storage
        vendor = storage.get('Vendor', self.vendor_id)
        return vendor.name
