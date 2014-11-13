'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import os
import logging
import datetime

from flask import Flask, request
from flask.ext.login import current_user
from cocktailor.home.models import Category, Menu, Order
from flask.ext.sqlalchemy import SQLAlchemy

from cocktailor.extensions import db

from sqlalchemy import create_engine


def create_app(config=None):
    """
    Creates the app.
    """

    app = Flask("cocktailor")
    app.config.from_object('cocktailor.configs.default.DefaultConfig')
    app.config.from_object(config)
    app.config.from_envvar("FLASKBB_SETTINGS", silent=True)
    
    configure_extensions(app)

    return app

def configure_extensions(app):
    db.init_app(app)
