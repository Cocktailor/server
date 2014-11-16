'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import json
from flask import Flask, redirect, url_for
from flask.ext.script import (Manager, Server)

from cocktailor.app import create_app
from cocktailor.extensions import db
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.utils.populate import create_test_data

from cocktailor.home.models import (Category, Menu)
from cocktailor.auth.models import (User)

from cocktailor.auth.views import login
app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("cs408.kaist.ac.kr", port=4418))


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
    
    
if __name__ == "__main__":
    manager.run()