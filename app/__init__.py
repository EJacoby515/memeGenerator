from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from app.config import Config
from app.api.routes import api
from app.site.routes import site
from app.authentication.routes import auth
from app.models import db as root_db, login_manager, ma
from app.helpers import JSONEncoder
from flask_cors import CORS
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app, resources  = {r'/api/*': {'origins': '*'}})

    

    app.register_blueprint(site)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    app.json_encoder = JSONEncoder
    app.config.from_object(Config)
    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, root_db)
login_manager.init_app(app)

