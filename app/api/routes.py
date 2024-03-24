from flask import Blueprint, jsonify
from app.helpers import token_required
from app.models import User,  Image as DBImage

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/user', methods=['GET'])
@token_required
def get_user(current_user_token):
    # Example route that returns user information for an authenticated user
    user = {
        'id': current_user_token.id,
        'email': current_user_token.email,
        'first_name': current_user_token.first_name,
        'last_name': current_user_token.last_name
    }
    return jsonify(user), 200

@api.route('/images')
def get_images():
    images = DBImage.query.all()
    image_data = [{'id': image.id, 'filename': image.filename} for image in images]
    return jsonify({'images': image_data})

@api.route('/images/<int:image_id>')
def get_image(image_id):
    image = DBImage.query.get_or_404(image_id)
    return jsonify({'id': image.id, 'filename': image.filename, 'data': image.data.decode('utf-8')})
