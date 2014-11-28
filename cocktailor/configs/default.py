'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import os

class DefaultConfig(object):
    
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
                              'cocktailor.sqlite'
    
    PICTURE_STORE_PATH = os.path.join(_basedir, 'resource')
    
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    
#     DEBUG = TRUE
#     TESTING = False

#    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/test'
#    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@cs408.kaist.ac.kr:4419/cocktailor'
    
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    MENU_URL_PREFIX = "/menu"
    USER_URL_PREFIX = "/user"
    AUTH_URL_PREFIX = "/auth"
    HOME_URL_PREFIX = "/home"
    API_URL_PREFIX = "/api"
    BLE_URL_PREFIX = "/bluetooth"

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"
    
        # Auth
    LOGIN_VIEW = "auth.login"
