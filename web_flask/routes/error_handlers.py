''' Defines the error blueprint '''
from flask import jsonify
from web_flask.routes import error_bp

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404