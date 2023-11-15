#!/usr/bin/python3
''' Defines the Vendor class '''
from sqlalchemy.ext.hybrid import hybrid_property
from web_flask import db
from models.base_model import BaseModel


class Vendor(BaseModel, db.Model):
    ''' Defines table for Vendor instances'''
    name = db.Column(db.String(120), index=True, nullable=False)
    email =  db.Column(db.String(120), index=True)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(120))
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'))
    orders = db.relationship('Order', backref='vendor', uselist=True,\
                             lazy=True)


    @hybrid_property
    def open_orders(self):
        ''' Returns the number of open/undelivered orders for a vendor '''
        return sum(1 for order in self.orders if not order.delivery_status)


    @hybrid_property
    def last_order(self):
        ''' Returns the last order for a Vendor instance '''
        if self.orders:
            sorted_orders = sorted(self.orders, key=lambda x: x.created_at,
                                   reverse=True)
            latest_order = sorted_orders[0]
            
            # Extract the datetime of the latest order
            date_time = latest_order.created_at
            date = date_time.strftime('%d/%m/%Y')
            return date
        return None
