'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import os
from flask import redirect, url_for, send_file
from flask.ext.script import (Manager, Server)

from cocktailor.app import create_app
from cocktailor.extensions import db
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.utils.populate import create_test_data

from cocktailor.auth.models import (User)

from flask.ext.login import current_user

from gcm import *

app = create_app(Config)
manager = Manager(app)

import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from cocktailor.configs.individualsettings import IndividualConfig as IConfig
manager.add_command("runserver", Server(IConfig.ServerAddress, port=4418))


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
    user.save()

    user = User()
    user.username = 'admin1'
    user.password = 'password'
    user.email = 'a@a.com'
    user.save()
    
    user = User()
    user.username = 'admin2'
    user.password = 'password'
    user.email = 'a@a.com'
    user.save()


@app.route('/')
def start():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('home.index'))
    return redirect(url_for('auth.login'))

_basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                os.path.dirname(__file__)))))
PICTURE_STORE_PATH = os.path.join(_basedir, 'resource')


@app.route('/api/picture/<string:fname>', methods=['GET'])
def picture_receive(fname):
    path = os.path.join(PICTURE_STORE_PATH, fname)
    return send_file(path, mimetype='image/gif')


if __name__ == "__main__":
    manager.run()
    
    
