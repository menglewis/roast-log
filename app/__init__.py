# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate
from settings import ProdConfig

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_object=ProdConfig):

    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    return None


def register_blueprints(app):
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/accounts')

    from .roast import roast as roast_blueprint
    app.register_blueprint(roast_blueprint)

    login_manager.login_view = "auth.login"

    return None
