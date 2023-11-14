''' Defines the user related routes '''
from flask import redirect, render_template, url_for, request, flash
from flask_login import current_user, login_required, logout_user
from web_flask.routes import user_views
from models import storage


@user_views.route("/logout")
@login_required
def logout():
    ''' Handles user logout '''
    logout_user()
    # flash("Successfully logged out")
    return redirect(url_for('pub_views.landing_page'))


@user_views.route('/', methods=['GET'])
@login_required
def dashboard():
    ''' Returns the user's dashboard page '''
    # flash('Welcome {}'.format(current_user.username))
    username = current_user.username
    tot_vendors = len(storage.all( username, 'Vendor'))
    tot_orders = len(storage.all( username, 'Order'))
    tot_reviews = len(storage.all(username, 'Review'))
    return render_template('/dashboard/dashboard.html', page="Dashboard",
                           tot_vendors=tot_vendors, tot_orders=tot_orders,
                           tot_reviews=tot_reviews)


@user_views.route('/search/', methods=['POST', 'GET'])
@login_required
def search():
    ''' Handles search operations '''
    from models.forms import SearchForm

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
            # saves searched word-'word' and class-'option' temporarily
            storage.word = word
            storage.option = option
        search_results = storage.do_search(word, option, username,\
                                           page, per_page)
        if option == 'Vendor':
            return render_template('/vendors/vendors.html',\
                search_results=search_results, page='Vendors',\
                username=username)
        if option == 'Order':
            return render_template('/orders/orders.html',\
                search_results=search_results, page='Orders')

    # Retrieves and redirect to the page user searched from
    current_page = request.form.get('current_pg', '/')
    if not form.searched.data:
        flash('Search word missing')
    if not form.option.data:
        flash('Select an option')
    return redirect(current_page)
