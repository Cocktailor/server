'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import os

class DefaultConfig(object):
    
#    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
#                            os.path.dirname(__file__)))))
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
#                              'cocktailor.sqlite'
    
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/test'
#    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@cs408.kaist.ac.kr:4419/cocktailor'
    
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False
