''' Defines the vendor related routes '''
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models import storage
from models.forms import VendorForm
from web_flask.routes import user_views


@user_views.route('/vendors')
@login_required
def vendors():
    ''' Retrieves all vendors of the current user 

        Return: vendors.html page with user's vendors
    '''
    page = request.args.get('page', 1, type=int)
    per_page = 12
    username = current_user.username

    pag_vendors = storage.do_paginate('Vendor', page, per_page, username)
    return render_template('/vendors/vendors.html', vendors=pag_vendors,\
                           page='Vendors')


@user_views.route('/vendors/new', methods=['GET', 'POST'])
@login_required
def create_vendor():
    ''' Handles new vendor creation for the current user '''
    form = VendorForm()

    # Pass current user's username to the form instance for validation
    form.current_user_username = current_user.username

    if form.validate_on_submit():
        vendor = storage.create_vendor(
            form.name.data, form.email.data, form.phone_number.data,
            form.address.data, str(current_user.get_id()))

        storage.new(vendor)
        storage.save()
        return redirect(url_for('user_views.vendors'))

    return render_template('/vendors/vendors.html', form=form,\
                           page='New Vendor')


@user_views.route('/vendors/<string:id>/view')
@login_required
def view_vendor(id):
    ''' Returns the view page of the user selected vendor '''
    username = current_user.username
    vendor = storage.get('Vendor', id)
    vendor_avr_review = storage.get_average_reviews(username, id)

    return render_template('/vendors/vendors.html', selected_vendor=vendor,\
                           page='Vendors', avr_review=vendor_avr_review)


@user_views.route('/vendors/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vendor(id):
    ''' Edits and updates an already existing vendor '''
    vendor = storage.get('Vendor', id)
    old_name = vendor.name
    old_email = vendor.email

    # Pre-fills the form with the old vendor information
    form = VendorForm(obj=vendor)

    # Set edit mode to True and passes the old name and email for validation
    form.edit_mode = True
    form.old_vendor_name = old_name
    form.old_vendor_email = old_email
    form.current_user_username = current_user.username

    if form.validate_on_submit():
        form.populate_obj(vendor)
        storage.save()
        return redirect(url_for('user_views.vendors'))

    return render_template('/vendors/vendors.html', form=form)


@login_required
@user_views.route('/vendors/<string:id>/delete', methods=['POST'] )
def delete_vendor(id):
    ''' Deletes a vendor with a given id '''
    storage.delete_from_db('Vendor', id)
    return redirect(url_for('user_views.vendors'))


@user_views.route('/vendors/<vendor_id>')
def get_vendor(vendor_id):
    ''' Retrieves a vendor and returns a dictionary/json format
        of a Vendor object (used by the JQuery to dynamically load
        preview section for a selected vendor in the vendor table)
    '''
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
    avr_review = storage.get_average_reviews(username, vendor_id)

    vendor_dict.update({'avr_review': avr_review})

    return vendor_dict
