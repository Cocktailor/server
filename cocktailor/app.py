'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from flask import Flask

from cocktailor.extensions import db, themes

from cocktailor.auth.views import auth



def create_app(config=None):
    """
    Creates the app.
    """

    app = Flask("cocktailor")
    app.config.from_object('cocktailor.configs.default.DefaultConfig')
    app.config.from_object(config)
    app.config.from_envvar("FLASKBB_SETTINGS", silent=True)
    
    configure_extensions(app)
    configure_blueprints(app)
    
    # Flask-Themes
    themes.init_themes(app, app_identifier="cocktailor")
    
    return app

def configure_extensions(app):
    db.init_app(app)

def configure_blueprints(app):
    app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])

    
