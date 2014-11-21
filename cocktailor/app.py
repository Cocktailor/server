'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from flask import Flask

# from flask.ext.login import current_user

from cocktailor.extensions import db, themes, login_manager

from cocktailor.auth.views import auth
from cocktailor.home.views import home
from cocktailor.menu.views import menu



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
    
    # Flask-Login
#     login_manager.login_view = app.config["LOGIN_VIEW"]
#     login_manager.refresh_view = app.config["REAUTH_VIEW"]
#     login_manager.anonymous_user = Guest

#     @login_manager.user_loader
#     def load_user(id):
#         """
#         Loads the user. Required by the `login` extension
#         """
#         unread_count = db.session.query(db.func.count(PrivateMessage.id)).\
#             filter(PrivateMessage.unread == True,
#                    PrivateMessage.user_id == id).subquery()
#         u = db.session.query(User, unread_count).filter(User.id == id).first()
#  
#         if u:
#             user, user.pm_unread = u
#             return user
#         else:
#             return None

#     login_manager.init_app(app)

def configure_blueprints(app):
    app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])
    app.register_blueprint(home, url_prefix=app.config["HOME_URL_PREFIX"])
    app.register_blueprint(menu, url_prefix=app.config["MENU_URL_PREFIX"])

    
