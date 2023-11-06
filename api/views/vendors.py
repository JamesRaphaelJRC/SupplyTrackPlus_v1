from flask import jsonify
from flask_login import current_user
from web_flask import app
from models import storage

@app.route('/user/vendors/<vendor_id>')
def get_vendor(vendor_id):
    ''' Retrieves a vendor '''
    vendor = storage.get('Vendor', vendor_id)
    last_order = vendor.last_order
    open_orders = vendor.open_orders
    total_orders = len(vendor.orders)
    closed_orders = total_orders - open_orders
    vendor_dict = vendor.to_dict()
    vendor_dict.update({'last_order': last_order})
    vendor_dict.update({'total_orders': total_orders})
    vendor_dict.update({'open_orders': open_orders})
    vendor_dict.update({'closed_orders': closed_orders})

    # Remove the unserializable orders of type Object
    del vendor_dict['orders']

    username = current_user.username

    vendor_reviews = [ review for review in storage.all(username, 'Review').\
                      values() if review.vendor_id == vendor_id]
    tot_rating = 0
    num_ratings = len(vendor_reviews) # Since every review must have a rating

    tot_rating = sum(review.rating for review in vendor_reviews)
    
    try:
        avr_review = tot_rating / num_ratings
    except ZeroDivisionError:
        avr_review = 0

    vendor_dict.update({'avr_review': avr_review})

    return vendor_dict
