''' Defines logics that apply to all routes '''
from flask_login import current_user
from models.forms import SearchForm
from models import storage
from web_flask import app

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
