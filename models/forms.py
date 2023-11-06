#!/usr/bin/python3
''' Defines forms used in the application '''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    RadioField
from wtforms import IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.validators import Optional
from models import storage


class LoginForm(FlaskForm):
    ''' Defines the login form '''
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remeber Me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    ''' Defines the sign-up form for new User registration '''
    first_name = StringField('First name*', validators=[DataRequired()])
    last_name = StringField('Last name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password*',
                                    validators=[DataRequired(),
                                                EqualTo('password')])
    phone_number = StringField('Mobile number (optional)')
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        ''' Checks if username already exists/used
            username.data fetches the username inputed in the SignUp form
        '''
        if storage.get_user(username.data):
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        ''' Checks if email already exists/used
            email.data fetches the email entered in the SignUp form
        '''
        if storage.check_email(email.data) is True:
            raise ValidationError('Please use a different email.')


class VendorForm(FlaskForm):
    ''' Defines a form for creation and validation of a new Vendor instance '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    phone_number = StringField('Mobile number')
    address = StringField('Address')
    submit = SubmitField('Done')

    current_user_username = None

    def validate_name(self, name):
        ''' Checks if vendor name already exists for the current user '''
        vendors = storage.all(self.current_user_username, 'Vendor')
        if vendors:
            if any(vendor.name == name.data for vendor in vendors.values()):
                raise ValidationError(
                    'Vendor already exists. Kindly consider another name')

    def validate_email(self, email):
        ''' Checks if a vendor with same email already exists for the current
            user
        '''
        vendors = storage.all(self.current_user_username, 'Vendor')
        if vendors:
            if any(vendor.email == email.data for vendor in vendors.values()):
                raise ValidationError('Email already exixts for a vendor')


class OrderForm(FlaskForm):
    ''' Defines the form for creation and validation of a new Order instance'''

    vendor_id = SelectField('Vendor', coerce=str)
    product_name = StringField('Product name*', validators=[DataRequired()])
    description = StringField('Product Description')
    quantity = IntegerField('Quantity*', validators=[DataRequired()])
    unit = StringField('Unit (e.g. Pair)')
    unit_cost = FloatField('Unit cost', validators=[Optional()])
    delivery_status = BooleanField('delivered?', default=False)
    submit = SubmitField('Done')


class ReviewForm(FlaskForm):
    ''' Defines the review form'''
    ratings = [0, 1, 2, 3, 4, 5]
    vendor_id = SelectField('Vendor', coerce=str, validators=[DataRequired()])
    order_id = SelectField('Order', coerce=str, validators=[DataRequired()])
    content = StringField('Review')
    rating = SelectField('Rating', validators=[DataRequired()], choices=ratings)
    submit = SubmitField('Done')


class SearchForm(FlaskForm):
    ''' Defines the search form '''
    searched = StringField('Searched', validators=[DataRequired()])
    option = RadioField("option", choices=[('Vendor', 'Vendor'), ('Order', 'Order')], validators=[DataRequired()])
    submit = SubmitField('Go')
