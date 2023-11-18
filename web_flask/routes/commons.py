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
        username = current_user.username
        user = storage.get_user(username)
        stats = storage.fetch_statistics(username)
        return dict(searchform=searchform, user=user, stats=stats)
    else:
        return dict(searchform=searchform)
