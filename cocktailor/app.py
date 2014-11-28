'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from flask import Flask

from cocktailor.extensions import db, themes, login_manager
from cocktailor.auth.models import User

from cocktailor.auth.views import auth
from cocktailor.home.views import home
from cocktailor.menu.views import menu
from cocktailor.api import api
from cocktailor.bluetooth.views import ble



def create_app(config=None):
    """
    Creates the app.
    """

    app = Flask("cocktailor")
    app.config.from_object('cocktailor.configs.default.DefaultConfig')
    app.config.from_object(config)
    app.config.from_envvar("COCKTAILOR_SETTINGS", silent=True)
    
    configure_extensions(app)
    configure_blueprints(app)
    
    # Flask-Themes
    themes.init_themes(app, app_identifier="cocktailor")
    
    return app

def configure_extensions(app):
    db.init_app(app)

    @login_manager.user_loader
    def load_user(u_id):
        """
        Loads the user. Required by the `login` extension
        """
        users = User.query.all()
        for u in users:
            if unicode(u.id) == u_id:
                return u
        return None

    login_manager.init_app(app)

def configure_blueprints(app):
    app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])
    app.register_blueprint(home, url_prefix=app.config["HOME_URL_PREFIX"])
    app.register_blueprint(menu, url_prefix=app.config["MENU_URL_PREFIX"])
    app.register_blueprint(api, url_prefix=app.config["API_URL_PREFIX"])
    app.register_blueprint(ble, url_prefix=app.config["BLE_URL_PREFIX"])

    
