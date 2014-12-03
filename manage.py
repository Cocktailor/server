'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from flask import redirect, url_for
from flask.ext.script import Manager, Server

from cocktailor.app import create_app
from cocktailor.extensions import db
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.configs.individualsettings import IndividualConfig as IConfig
from cocktailor.utils.populate import create_test_data
from cocktailor.auth.models import User
# from cocktailor.call.models import FunctionalCallName, WaiterCall
from flask.ext.login import current_user

from gcm import *

import logging, sys

app = create_app(Config)
manager = Manager(app)


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


manager.add_command("runserver", Server(IConfig.ServerAddress, port=IConfig.ServerPort))

@manager.command
def test():
    return 'a'

@manager.command
def testgcm():
    print 'yoyo'
    gcm = GCM('AIzaSyBsDGUDh_5O5O-BqipGljNLQMurQNRgP2M')
    data = {'device_id': '18:22:7E:BD:F3:85'}
    reg_id = 'APA91bEIn5sG1nUTtL_5hIo4vgvxVufj64iie9OgYWvhMkA_75mHu1OVU7ax4307TDWQA6fGKQ1yObrRdKrO-SLPvyjB5m_-OtdGm_KHFO0n13-qbSyC3qCrK8Q5lGKWx4PcG5yd6GxxgtIywrbMTts6O85FiG0aYA'
    gcm.plaintext_request(registration_id=reg_id, data=data)
    print 'yoyo'

@manager.command
def createall(dropdb=False, createdb=False):
    """Creates the database with some testing content.
    If you do not want to drop or create the db add
    '-c' (to not create the db) and '-d' (to not drop the db)
    """
    
    db.drop_all()
    db.create_all()
    create_test_data()

    user = User()
    user.username = 'admin'
    user.password = 'password'
    user.email = 'a@a.com'
    user.restaurant_id = 1
    user.save()

    user = User()
    user.username = 'admin1'
    user.password = 'password'
    user.email = 'a1@a.com'
    user.restaurant_id = 2
    user.save()
    
    user = User()
    user.username = 'admin2'
    user.password = 'password'
    user.email = 'a2@a.com'
    user.restaurant_id = 3
    user.save()

@app.route('/')
def start():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    return redirect(url_for('menu.index'))

if __name__ == "__main__":
    manager.run()
    
    
