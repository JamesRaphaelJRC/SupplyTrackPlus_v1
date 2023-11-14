''' Defines the reviews routes '''
from flask import render_template, redirect, request, url_for,\
    flash
from flask_login import login_required, current_user
from models import storage
from models.forms import ReviewForm
from web_flask.routes import user_views


@user_views.route('/reviews', methods=['GET'])
@login_required
def reviews():
    '''' Processes and returns user reviews '''
    username = current_user.username
    page = request.args.get('page', 1, type=int)
    per_page = 4
    if request.method == 'GET':
        pag_reviews = storage.do_paginate('Review', page, per_page, username)
        return render_template('/reviews/reviews.html', page='Reviews',\
                               reviews=pag_reviews)


@user_views.route('/reviews/new', methods=['GET', 'POST'])
@login_required
def create_review():
    ''' Handles review creation operations '''
    form = ReviewForm()
    username = current_user.username

    # Gets vendor_id and order_id when this function is called from order page
    vendor_id = request.args.get("vendor_id")
    if vendor_id:
        form.vendor_id.choices = (storage.get('Vendor', vendor_id).name, )
        selected_vendor = vendor_id
    else:
        # When called from reviews page
        vendors = [(v.id, v.name) for v in storage.all(username, 'Vendor').\
                   values()]
        vendors.insert(0, ("", "Select vendor"))
        form.vendor_id.choices = vendors
        selected_vendor = form.vendor_id.data

    order_id = request.args.get("order_id")
    if order_id:
        form.order_id.choices = (storage.get('Order', order_id).product_name, )
        selected_order = order_id
    else:
        orders = [(o.id, o.product_name) for o in storage.\
                  all(username, 'Order').values() if o.\
                    vendor_id == selected_vendor and o.delivery_status == True]
        orders.insert(0, ("", "Select delivered order"))
        form.order_id.choices = orders

    if form.validate_on_submit() and request.method == 'POST':
        selected_order = form.order_id.data
        
        if selected_vendor == "" or selected_order == "":
            if selected_vendor == "":
                flash("Please select a vendor")
            if selected_order == "":
                flash("Please select an order")
            return render_template('/reviews/reviews.html', form=form, page='Reviews',
                                   username=username)
        review = storage.create_review(
            form.content.data, selected_vendor, selected_order,
            current_user.get_id(), form.rating.data)
        storage.new(review)
        storage.save()
        return redirect(url_for('user_views.reviews'))

    return render_template('/reviews/reviews.html', form=form, page='Reviews')


@user_views.route('/reviews/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    ''' Edits a review with a given id '''
    review = storage.get('Review', id)
    form = ReviewForm(obj=review)
    username = current_user.username
    vendors = [(v.id, v.name) for v in storage.all(username, 'Vendor').\
               values()]
    form.vendor_id.choices = vendors
    selected_vendor = form.vendor_id.data
    orders = [(o.id, o.product_name) for o in storage.all(username, 'Order').\
              values() if o.vendor_id == selected_vendor]
    form.order_id.choices = orders

    if form.validate_on_submit() and request.method == 'POST':
        selected_order = form.order_id.data
        if selected_vendor == "" or selected_order == "":
            if selected_vendor == "":
                flash("Please select a vendor")
            if selected_order == "":
                flash("Please select an order")
            return render_template('/reviews/reviews.html', page='Reviews',\
                                   username=username)
        form.populate_obj(review)
        storage.save()
        return redirect(url_for('user_views.reviews'))

    return render_template('/reviews/reviews.html', form=form, page='Reviews')


@user_views.route('/reviews/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review(id):
    ''' Deletes a review with a given id '''
    review = storage.get('Review', id)
    storage.delete_from_db(review, id)
    storage.save()
    return redirect(url_for('user_views.reviews'))




