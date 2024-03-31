from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
from marshmallow  import  fields
import secrets
from sqlalchemy import LargeBinary
from app.models import db, Image as DBImage
from app.helpers import token_required
from flask import Blueprint, jsonify, request
import base64

api = Blueprint('api', __name__, url_prefix='/api')

# User Routes

# GET route to fetch all users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_data = [{'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in users]
    return jsonify({'users': user_data})

# POST route to create a new user
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json  # Assuming request body contains JSON data
    new_user = User(email=data.get('email'), first_name=data.get('first_name'), last_name=data.get('last_name'), password=data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# PUT route to update an existing user
@api.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json  # Assuming request body contains JSON data
    user.email = data.get('email', user.email)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# DELETE route to delete an existing user
@api.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Image Routes

# GET route to fetch all images
@api.route('/images', methods=['GET'])
def get_images():
    images = DBImage.query.all()
    print(f"Retrieved {len(images)} images from the database")
    
    image_data = []
    for image in images:
        print(f"Processing image: {image.id}")
        if image.data is not None:
            encoded_data = base64.b64encode(image.data).decode('utf-8')
            print(f"Encoded data: {encoded_data[:20]}...")  # Print the first 20 characters of encoded data
        else:
            print("Image data is None")
            encoded_data = None
        
        image_data.append({'id': image.id, 'filename': image.filename, 'data': encoded_data, 'user_id': image.user_id})
    
    print(f"Returning {len(image_data)} images")
    return jsonify({'images': image_data})



# POST route to create a new image
@api.route('/images', methods=['POST'])
def create_image():
    if 'file' in request.files:
        image = request.files['file']
        filename = request.form.get('filename')  # Get filename from form data
        user_id = request.form.get('user_id')  # Get user_id from form data
        
        # Read image data and encode it to base64
        img_data = base64.b64encode(image.read()).decode('utf-8')

        # Create a new Image instance and add it to the database
        new_image = image(filename=filename, data=img_data, user_id=user_id)
        db.session.add(new_image)
        db.session.commit()

        # Return success message with image details
        return jsonify({'message': 'Image created successfully', 'image_id': new_image.id, 'filename': new_image.filename, 'user_id': new_image.user_id}), 201
    else:
        # Return error message if no file is provided
        return jsonify({'error': 'No file provided'}), 400

# PUT route to update an existing image
@api.route('/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = DBImage.query.get_or_404(image_id)
    data = request.json  # Assuming request body contains JSON data
    image.filename = data.get('filename', image.filename)
    image.user_id = data.get('user_id', image.user_id)
    db.session.commit()
    return jsonify({'message': 'Image updated successfully'}), 200

# DELETE route to delete an existing image
@api.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = DBImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Image deleted successfully'}), 200