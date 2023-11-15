''' Defines public routes that does not require user authentication '''
from flask import render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse 
from models.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user
from models import storage
from web_flask.routes import pub_views


@pub_views.route('/')
def landing_page():
    ''' Returns the landing/welcome page '''
    return render_template('index.html', page='Home')


@pub_views.route('/about')
def about():
    ''' Returns the about page '''
    return render_template('about.html', page='About')


@pub_views.route('/signUp', methods=['GET', 'POST'])
def signUp():
    ''' Handles the creation of new User object '''
    if current_user.is_authenticated:
        return redirect(url_for('user_views.dashboard'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = storage.create_user(
            form.first_name.data, form.last_name.data, form.email.data,
            form.username.data, form.password.data, form.phone_number.data)
        storage.new(user)
        storage.save()
        flash('Registration was successful, congratulations!')
        return redirect(url_for('pub_views.login'))
    return render_template('signUp.html', form=form)


@pub_views.route('/login', methods=['GET', 'POST'])
def login():
    '''' Processes user login by validating user's login credentials '''
    if current_user.is_authenticated:
        return redirect(url_for('user_views.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        if storage.validate_user(form.username.data, form.password.data):
            user = storage.get_user(form.username.data)

            # Creates a login session for the validated user
            login_user(user, remember=form.remember_me.data)

            # Retrieves the page in cases where user tries to access a
            # previously visited page after logging out
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for("user_views.dashboard")
            return redirect(next_page)

        flash('Incorrect Username or Password')
        # Prevents re-submission during page refresh
        return redirect(url_for('pub_views.login'))

    return render_template('login.html', form=form)
