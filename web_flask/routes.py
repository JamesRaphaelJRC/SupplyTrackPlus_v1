#!/usr/bin/python3
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from models.forms import *
from web_flask import app
from models import storage
from api.views.vendors import *


@app.route('/')
def landing_page():
    return render_template('index.html', page='Home')


@app.route('/about')
def about():
    ''' Returns the about page '''
    return render_template('about.html', page='About')


@app.route('/user/profile')
def profile():
    ''' Returns the user profile page '''
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''' Processes user login by validating user's login credentials '''
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        if storage.validate_user(form.username.data, form.password.data):
            user = storage.get_user(form.username.data)

            # Creates a login session for the validated user
            login_user(user, remember=form.remember_me.data)
            # flash('Login successful!')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard')
            return redirect(next_page)
        flash('Incorrect Username or Password')
        # Prevents re-submission during page refresh
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/user/logout")
@login_required
def logout():
    ''' Handles user logout '''
    logout_user()
    # flash("Successfully logged out")
    return redirect(url_for('landing_page'))


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    ''' Handles the creation of new User object '''
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = storage.create_user(
            form.first_name.data, form.last_name.data, form.email.data,
            form.username.data, form.password.data, form.phone_number.data)
        storage.new(user)
        storage.save()
        flash('Registration was successful, congratulations!')
        return redirect(url_for('login'))
    return render_template('signUp.html', form=form)


@app.route('/user', methods=['GET'])
@login_required
def dashboard():
    ''' Returns the user's dashboard page '''
    # flash('Welcome {}'.format(current_user.username))
    username = current_user.username
    tot_vendors = len(storage.all( username, 'Vendor'))
    tot_orders = len(storage.all( username, 'Order'))
    tot_reviews = len(storage.all(username, 'Review'))
    return render_template('dashboard.html', page="Dashboard",
                           tot_vendors=tot_vendors, tot_orders=tot_orders,
                           tot_reviews=tot_reviews)


@app.route('/user/vendors')
@login_required
def vendors():
    ''' Returns all vendors of the current user '''
    # user_id = current_user.get_id()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    username = current_user.username
    pag_vendors = storage.do_paginate('Vendor', page, per_page, username)
    return render_template('vendors.html', vendors=pag_vendors, page='Vendors')


@app.route('/user/vendors/new', methods=['GET', 'POST'])
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
        return redirect(url_for('vendors'))
    return render_template('vendors.html', form=form, page='New Vendor')


@app.route('/user/vendors/<string:id>/view')
@login_required
def view_vendor(id):
    ''' Returns the view page of the selected vendor '''
    username = current_user.username
    vendor = storage.get('Vendor', id)
    vendor_avr_review = storage.get_average_reviews(username, id)
    return render_template('vendors.html', selected_vendor=vendor,\
                           page='Vendors', avr_review=vendor_avr_review)


@app.route('/user/vendors/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vendor(id):
    ''' Edit and updates an already existing vendor '''
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
        return redirect(url_for('vendors'))
    return render_template('vendors.html', form=form)


@login_required
@app.route('/user/vendors/<string:id>/delete', methods=['POST'] )
def delete_vendor(id):
    ''' Deletes a vendor with a given id '''
    storage.delete_from_db('Vendor', id)
    return redirect(url_for('vendors'))


@app.route('/user/orders/', methods=['GET', 'POST'])
def orders():
    ''' Handles order operations '''
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 12
        username = current_user.username
        pag_orders = storage.do_paginate('Order', page, per_page, username)
        return render_template('orders.html', orders=pag_orders,
                            page='Orders')
    if request.method == 'POST':
        ''' Processes marking order as reveived '''
        order_id  = request.args.get('id')
        print(order_id)
        order = storage.get('Order', str(order_id))
        order.delivery_status = True
        storage.save()
        return redirect(url_for('orders'))


@app.route('/user/orders/filter_by/', methods=['GET', 'POST'])
@login_required
def filter_orders():
    ''' Returns user Order objects based on filter word '''
    if request.method == 'POST':
        filter_by = request.form.get('filter_by')
    if request.method == 'GET':
        # For request coming from the next_page pagination link in orders.html
        filter_by = request.args.get('filter_by')

    page = request.args.get('page', 1, type=int)
    per_page = 12
    username = current_user.username
    pag_orders = storage.do_paginate('Order', page, per_page, username,\
                                     filter=filter_by)
    return render_template('orders.html', orders=pag_orders,
                        page='Orders', filter_by=filter_by)

@app.route('/user/orders/new', methods=['GET', 'POST'])
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
        return redirect(url_for('orders'))
    return render_template('orders.html', form=form, page='Orders')


@app.route('/user/orders/<string:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('orders'))
    return render_template('orders.html', form=form, page='Orders')


@app.route('/user/orders/<string:id>/delete', methods=['POST'])
@login_required
def delete_order(id):
    ''' Deletes an order with a given id '''
    storage.delete_from_db('Order', id)
    return redirect(url_for('orders'))



@app.route('/user/reviews/', methods=['GET'])
@login_required
def reviews():
    '''' Processes and returns user reviews '''
    username = current_user.username
    page = request.args.get('page', 1, type=int)
    per_page = 4
    if request.method == 'GET':
        pag_reviews = storage.do_paginate('Review', page, per_page, username)
        return render_template('reviews.html', page='Reviews',\
                               reviews=pag_reviews)


@app.route('/user/reviews/new', methods=['GET', 'POST'])
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
            return render_template('reviews.html', form=form, page='Reviews',
                                   username=username)
        review = storage.create_review(
            form.content.data, selected_vendor, selected_order,
            current_user.get_id(), form.rating.data)
        storage.new(review)
        storage.save()
        return redirect(url_for('reviews'))

    return render_template('reviews.html', form=form, page='Reviews')


@app.route('/get_orders/<vendor_id>')
def get_orders(vendor_id):
    ''' Returns the Orders of a given vendor for a given user '''
    orders = [(o.id, o.product_name) for o in storage.all(\
        current_user.username, 'Order').values() if o.vendor_id == vendor_id\
            and o.delivery_status == True]
    return jsonify(orders)


@app.route('/user/review/<string:id>/edit', methods=['GET', 'POST'])
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
            return render_template('reviews.html', page='Reviews',\
                                   username=username)
        form.populate_obj(review)
        storage.save()
        return redirect(url_for('reviews'))

    return render_template('reviews.html', form=form, page='Reviews')


@app.route('/user/review/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review(id):
    ''' Deletes a review with a given id '''
    review = storage.get('Review', id)
    storage.delete_from_db(review, id)
    storage.save()
    return redirect(url_for('reviews'))


@app.context_processor
def base():
    ''' Passes variables to all templates used in the app '''
    searchform = SearchForm()

    # Avoid passing user obj to public pages e.g. login, signup and index pages
    if current_user.is_authenticated:
        user = storage.get_user(current_user.username)
        return dict(searchform=searchform, user=user)
    else:
        return dict(searchform=searchform)


@app.route('/user/search/', methods=['POST', 'GET'])
@login_required
def search():
    ''' Handles search operations '''
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    username = current_user.username
    if form.validate_on_submit() or request.method == 'GET':
        if request.method == 'GET':
            # retrieves temp stored word and option for pagination
            word = storage.word
            option = storage.option
        else:
            word = form.searched.data
            option = form.option.data
            # saves searched word 'word' and class, 'option' temporarily
            storage.word = word
            storage.option = option
        search_results = storage.do_search(word, option, username,\
                                           page, per_page)
        if option == 'Vendor':
            return render_template('vendors.html',\
                search_results=search_results, page='Vendors',\
                username=username)
        if option == 'Order':
            return render_template('orders.html',\
                search_results=search_results, page='Orders')

    # Retrieves the page user searched from
    current_page = request.form.get('current_pg', '/')
    if not form.searched.data:
        flash('Search word missing')
    if not form.option.data:
        flash('Select an option')
    return redirect(current_page)
    

# @app.route('/user/settings/')
# @login_required
# def settings():
#     ''' Returns the user settings page '''
#     pass


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404
