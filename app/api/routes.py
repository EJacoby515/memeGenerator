from flask import Blueprint, jsonify
from app.helpers import token_required
from app.models import User

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/user_info', methods=['GET'])
@token_required
def get_user_info(current_user_token):
    # Example route that returns user information for an authenticated user
    user_info = {
        'id': current_user_token.id,
        'email': current_user_token.email,
        'first_name': current_user_token.first_name,
        'last_name': current_user_token.last_name
    }
    return jsonify(user_info), 200
