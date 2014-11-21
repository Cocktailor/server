'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import json
from flask import Flask, redirect, url_for
from flask.ext.script import (Manager, Server)

from cocktailor.app import create_app
from cocktailor.extensions import db, login_manager
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.utils.populate import create_test_data

from cocktailor.menu.models import (Category, Menu)
from cocktailor.auth.models import (User)

from flask.ext.login import current_user

from cocktailor.auth.views import login,auth
from cocktailor.home.views import home
from flask.globals import request
from gcm import *


app = create_app(Config)
manager = Manager(app)

import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Run local server
# manager.add_command("runserver", Server("cs408.kaist.ac.kr", port=4418))
manager.add_command("runserver", Server("localhost", port=4418))


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

@app.route('/')
def start():
#     if current_user is not None and current_user.is_authenticated():
#         return redirect(url_for('home.index'))
    return redirect(url_for('auth.login'))

@app.route('/fileupload')
def start():
#     if current_user is not None and current_user.is_authenticated():
#         return redirect(url_for('home.index'))
    return redirect(url_for('auth.login'))

@app.route('/menu_receive', methods=['GET'])
def menu_receive():
    categories = Category.query.all()
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())

    menus = Menu.query.all()
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    result = {}
    result['category'] = CategoriesArray
    result['menu'] = MenusArray
#     print(result)
    jsonString = json.dumps(result,sort_keys=True)
    return jsonString


@app.route('/picture/<picture>')
def show_picture(picture):
    print picture
    return '55'

@app.route('/api/register_user', methods=['POST'])
def register_user():
    device_id = request.form['device_id']
    reg_id = request.form['reg_id']
    iswaiter = request.form['iswaiter']

    print 'device_id(' + device_id + ') reg_id(' + reg_id + ') waiter(' + iswaiter + ')' 
    
    user = User.query.filter_by(device_id=device_id).first()
    if user is None:
        user = User()
    
    if len(device_id) != 0 :
        user.device_id = device_id
    if len(reg_id)  != 0 :
        user.reg_id = reg_id
    if len(iswaiter) != 0 :
        user.iswaiter = iswaiter
    user.save()
    
    return "", 200
    
@app.route('/api/call_waiter', methods=['POST'])
def call_waiter():
    ble_id = request.form['ble_id']
    table = request.form['table']

    print 'ble_id(' + ble_id + ') table(' + table + ')'
    
    user = User.query.filter_by(ble_id=ble_id).first()
    if user is None:
        user = User()
    
    if len(ble_id) != 0 :
        user.ble_id = ble_id
    if len(table)  != 0 :
        user.table = table
    user.save()
    
    users = User.query.filter_by(iswaiter="Y")
    
    return "", 200
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    manager.run()
    
    
    
    
