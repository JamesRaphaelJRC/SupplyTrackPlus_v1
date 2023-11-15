''' Defines the orders routes '''
from flask import render_template, redirect, request, url_for,\
    flash, jsonify, session
from flask_login import login_required, current_user
from models import storage
from models.forms import OrderForm
from web_flask.routes import user_views


@user_views.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    ''' Retrives all user orders.
    
        Return: orders.html template with user's orders
    '''
    # Gets and save current page to user session for easy redirection
    session['history'] = session.get('history', [])
    session['history'].append(request.url)

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 12
        username = current_user.username
        pag_orders = storage.do_paginate('Order', page, per_page, username)
        return render_template('/orders/orders.html', orders=pag_orders,
                            page='Orders')

    if request.method == 'POST':
        ''' Processes marking an order as reveived by a user '''
        order_id  = request.args.get('id')
        order = storage.get('Order', str(order_id))
        order.delivery_status = True
        storage.save()
        return redirect(url_for('user_views.orders'))


@user_views.route('/orders/<string:id>/view')
@login_required
def view_order(id):
    ''' Returns the html template for a single user selected order '''

    # Gets and save current page to user session for easy redirection
    session['history'] = session.get('history', [])
    session['history'].append(request.url)

    order = storage.get('Order', id)
    return render_template('/orders/view_order.html', page='Orders',
                           order=order)


@user_views.route('/orders/filter_by/', methods=['GET', 'POST'])
@login_required
def filter_orders():
    ''' Returns a user Order objects based on filter word '''
    if request.method == 'POST':
        filter_by = request.form.get('filter_by')

    # For request coming from the next_page pagination link in orders.html
    if request.method == 'GET':
        filter_by = request.args.get('filter_by')

    # Group orders according to their vendors
    if filter_by == 'vendor':
        username = current_user.username
        vendors = storage.all(username, 'Vendor')
        orders = storage.all(username, 'Order')

        grouped_orders = {}
        for vendor in vendors.values():
            grouped_orders[vendor.name] = []
            for order in orders.values():
                if vendor.id == order.vendor_id:
                    grouped_orders[vendor.name].append(order)
        return render_template('orders/grouped_orders.html', page='Orders',
                               grouped_orders=grouped_orders)

    page = request.args.get('page', 1, type=int)
    per_page = 12
    username = current_user.username
    pag_orders = storage.do_paginate('Order', page, per_page, username,\
                                     filter=filter_by)
    return render_template('/orders/orders.html', orders=pag_orders,
                        page='Orders', filter_by=filter_by)


@user_views.route('/orders/get_orders/<vendor_id>')
def get_orders(vendor_id):
    ''' Returns the Orders of a given vendor for the current user '''
    orders = [(o.id, o.product_name) for o in storage.all(\
        current_user.username, 'Order').values() if o.vendor_id == vendor_id\
            and o.delivery_status == True]
    return jsonify(orders)


@user_views.route('/orders/new', methods=['GET', 'POST'])
@login_required
def create_order():
    ''' Handles new vendor creation for the current user '''
    form = OrderForm()
    vendors = [(v.id, v.name) for v in storage.\
               all(current_user.username, 'Vendor').values()]
    vendors.insert(0, ("", "Select vendor"))
    form.vendor_id.choices = vendors

    if form.validate_on_submit():
        vendor_id = form.vendor_id.data
        if vendor_id == "":
            flash("Please select a vendor")

            # Return the orders.html page with the form bearing previous inputs
            return render_template('orders.html', form=form)

        order = storage.create_order(
            form.product_name.data, form.description.data, form.quantity.data,
            form.unit.data, form.unit_cost.data, form.delivery_status.data,
            current_user.get_id(), form.vendor_id.data)

        storage.new(order)
        storage.save()
        return redirect(url_for('user_views.orders'))

    return render_template('/orders/orders.html', form=form, page='Orders')


@user_views.route('/orders/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    ''' Edits and updates an already existing order '''
    order = storage.get('Order', id)
    username = current_user.username

    # Pre-fills the form with the old order information
    form = OrderForm(obj=order)
    vendors = [(v.id, v.name) for v in storage.all(\
        username, 'Vendor').values()]
    vendors.insert(0, ("", "Select vendor"))
    form.vendor_id.choices = vendors

    if form.validate_on_submit() and request.method == 'POST':
        vendor_id = form.vendor_id.data
        if vendor_id == "":
            flash("Please select a vendor")
            return render_template('orders.html', form=form, page='Orders')
        form.populate_obj(order)
        storage.save()

        # Gets the page user processed edit from and redirects back to it
        prev_page = session.get('history')
        prev_page = prev_page[-1]
        return redirect(prev_page)

    return render_template('/orders/orders.html', form=form, page='Orders')


@user_views.route('/orders/<string:id>/delete', methods=['POST'])
@login_required
def delete_order(id):
    ''' Deletes an order with a given id '''
    storage.delete_from_db('Order', id)
    return redirect(url_for('user_views.orders'))
