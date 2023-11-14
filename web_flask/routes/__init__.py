from flask import Blueprint

user_views = Blueprint('user_views', __name__, url_prefix='/user')
pub_views = Blueprint('pub_views', __name__, template_folder='../templates/public/')
error_bp = Blueprint('error_bp', __name__, template_folder='../templates/errors/')
commons = Blueprint('commons', __name__)

from web_flask.routes.user import *
from web_flask.routes.vendors import *
from web_flask.routes.orders import *
from web_flask.routes.reviews import *
from web_flask.routes.commons import *
from web_flask.routes.public import *
from web_flask.routes.error_handlers import *
