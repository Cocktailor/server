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
    
    DEBUG = False
    TESTING = False

#     SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/test'
#    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@cs408.kaist.ac.kr:4419/cocktailor'
    
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

#     FORUM_URL_PREFIX = ""
    USER_URL_PREFIX = "/user"
    AUTH_URL_PREFIX = "/auth"
#     ADMIN_URL_PREFIX = "/admin"
    HOME_URL_PREFIX = "/home"

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"
