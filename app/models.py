# imports 
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
import base64

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)


    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
# class for image  DB
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)

    def __init__(self, filename, data, user_id):
        self.filename = filename
        self.data = base64.b64decode(data)
        self.user_id = user_id

    def __repr__(self):
        return f"Image(id={self.id}, filename={self.filename}, user_id = {self.user_id})"

    @classmethod
    def delete_image(cls,image_id):
        image = cls.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()


    @classmethod
    def update_image(cls, image_id,  new_filename):
        image = cls.query.get(image_id)
        if image:
            image.filename = new_filename
            db.session.commit()

