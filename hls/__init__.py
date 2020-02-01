import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

####################################################
### Config
####################################################
db = SQLAlchemy()
#login_manager = LoginManager()
#login_manager.login_view = 'root.index'


####################################################
### App Factory
####################################################
def create_app(cf=None):
    print("config at: " + cf)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(cf)
    initialize_extensions(app)
    register_blueprints(app)

    #migration support
    Migrate(app,db)

    return app


# attach app
def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


# load blue  prints
def register_blueprints(app):
#    from <app>.<module>.views import <module>_bp

#    app.register_blueprint(module_bp, url_prefix='/module')
#    from <app> import views
