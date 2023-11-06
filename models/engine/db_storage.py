#!/usr/bin/python3
''' Defines the DBStorage class '''
from web_flask import db
from models.user import User
from models.vendor import Vendor
from models.order import Order
from models.review import Review


class DBStorage:
    ''' Defines methods that interact with the database '''

    # Temporary storage for user's search word 'word' and class 'option'
    word = ""
    option = ""

    # Used by the globals() to convert classname in str to actual class
    classes = [User, Vendor, User, Order]

    def create_user(self, first, last, email, username, passwd, phone_no):
        ''' Creates a new User object, generates a password_hash with the
            user's password and updates it to the current user object

            Return:
                The newly created User object
        '''
        new_user = User(first_name=first, last_name=last, email=email,
                        username=username, password_hash=passwd,
                        phone_number=phone_no)
        new_user.set_password(passwd)
        return new_user


    def create_vendor(self, name, email, phone_no, address, user_id):
        ''' Creates and returns a new Vendor object '''
        new_vendor = Vendor(name=name, email=email, phone_number=phone_no,
                            address=address, user_id = user_id)
        return new_vendor


    def create_order(self, product, desc, qty, unit, cost, status, u_id, v_id):
        ''' Creates a new order
            Arguments:
                        product - product_name, des - description,
                        qty - quantity, unit - unit, cost - unit_cost,
                        status - delivery status, u_id - user_id
                        v_id - vendor_id
        '''
        new_order = Order(product_name=product, description=desc, quantity=qty,
                          unit=unit, unit_cost=cost, delivery_status=status,
                          user_id=u_id, vendor_id=v_id)
        return new_order


    def create_review(self, content, v_id, o_id, u_id, rating):
        ''' Creates a Review object and returns the created object '''
        new_review = Review(content=content, vendor_id=v_id, order_id=o_id,\
                            user_id=u_id, rating=rating)
        return new_review


    def validate_user(self, username, password):
        ''' Validates a user credentials
            Returns:
                    False - If username or email is not registered or password
                            is invalid
                    True -  If credentials are valid
        '''
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User.query.filter_by(email=username).first()
            if not user:
                return False
        passwd = user.check_password(password)
        if passwd:
            return True
        return False


    def check_email(self, email):
        ''' Checks if email already exists in the database.
            Return:
                    True if email already exists
                    False if email does not exist in the database
        '''
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        return False


    def get_user(self, username):
        ''' Gets a User object from the database using the unique username '''
        if username:
            user = User.query.filter_by(username=username).first()
            return user


    def open_orders(self, username):
        ''' Returns the number of open/undelivered orders
            made by a given user
        '''
        user_id = self.get_user(username).id
        open_orders = Order.query.filter_by(user_id=user_id,\
                                            delivery_status=False).all()
        return len(open_orders)


    def all(self, username, cls):
        ''' Returns a dictionary of all objects of a given class for a
            user

            return format: {<class>.<object_id>: object}
        '''
        if cls and username:
            user_id = self.get_user(username).id
            if type(cls) is str:
                # converts to the actual class if cls is a string.
                cls = globals()[cls]

            obj_dict = {}
            instances = cls.query.filter_by(user_id=user_id).all()

            for instance in instances:
                key = "{}.{}".format(type(instance).__name__, instance.id)
                obj_dict[key] = instance
            return obj_dict
        
        return None


    def do_paginate(self, cls, page, per_page, username, filter="latest"):
        ''' Returns a paginated object

            cls = object class            
            page = page number
            per_page =  Number of rows objects to be returned at a go
                        which is to be displayed per page
            username =  The username of the user whose objects are to be
                        returned
        '''
        filters = {"latest": 'cls.created_at.desc()', "oldest": 'cls.created_at',\
            "open": 'cls.delivery_status == True',\
            "closed": 'cls.delivery_status == False' }
        if cls:
            user_id = self.get_user(username).id
            if type(cls) is str:
                cls = globals()[cls]

            if filter in filters:
                keyword = filters.get(filter)
                return cls.query.filter_by(user_id=user_id).order_by(\
                    eval(keyword)).paginate(page=page, per_page=per_page,\
                                                    error_out=False)


    def do_search(self, search_word, option, username, page, per_page):
        ''' Handles search operations in the database 

            option: The class to search in.
            Return: A list of paginated objects containing the search_word
        '''
        cls = globals()[option]
        user_id = self.get_user(username).id

        if cls == Vendor:
            vendors = Vendor.query.filter_by(user_id=user_id)
            vendors = vendors.filter(Vendor.name.like(\
                '%' + search_word + '%'))
            vendors = vendors.order_by(Vendor.name).paginate(page=page,\
                            per_page=per_page, error_out=False)
            return vendors
        elif cls == Order:
            orders = Order.query.filter_by(user_id=user_id)
            orders = orders.filter(Order.product_name.like(\
                '%' + search_word + '%'))
            orders = orders.order_by(Order.product_name).paginate(page=page,\
                            per_page=per_page, error_out=False)
            return orders


    def new(self, obj):
        ''' Adds an object to the current database session '''
        db.session.add(obj)


    def save(self):
        ''' Commits all changes in the database session '''
        db.session.commit()


    def delete(self, obj):
        ''' Deletes an object from the current database session '''
        db.session.delete(obj)


    def delete_from_db(self, cls, id):
        ''' Deletes an object of a given class, for a given user from the
            database
        '''
        if cls and id:
            if type(cls) == str:
                cls = globals()[cls]
            try:
                obj = cls.query.get(id)
                if obj:
                    self.delete(obj)
                    self.save()
                    return True
                else:
                    return None
            except Exception as e:
                db.session.rollback()
                return False


    def get(self, cls, id):
        ''' Retrieves a single object of a class with a given id '''
        if type(cls) == str:
            cls = globals()[cls]

        if cls and id:
            obj = cls.query.get(id)
            return obj
        return None
