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

app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("cs408.kaist.ac.kr", port=4417))


@manager.command
def test():
    return 'a'

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

@app.route('/api/register_user', methods=['POST'])
def regid():
    device_id = request.form['device_id']
    reg_id = request.form['reg_id']
    waiter = request.form['waiter']
    
    user = User.query.filter_by(device_id=device_id)
    if len(user) == 0:
        user = User()
    else:
        user = user.first()
    
    if len(device_id) != 0 :
        user.device_id = device_id
    if len(reg_id)  != 0 :
        user.reg_id = reg_id
    if len(waiter) != 0 :
        user.waiter = waiter
    user.save()
    
    return "", 200
    
    
if __name__ == "__main__":
    manager.run()
    
    
    
    
    
    