'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

import json
from flask import Flask
from flask import render_template;
from flask.ext.script import (Manager, Server)

from cocktailor.app import create_app
from cocktailor.extensions import db
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.utils.populate import create_test_data

from cocktailor.home.models import (Category, Menu)

app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("localhost", port=4418))


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


# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Logs the user in."""
#     print("aaa??")
#     error = None
#     if request.method == 'POST':
#         print('10')
#     else:
#         return render_template('login.html', error=error)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Logs the user in."""
#     if g.user:
#         return redirect(url_for('timeline'))
#     error = None
#     if request.method == 'POST':
#         user = query_db('''select * from user where
#             username = ?''', [request.form['username']], one=True)
#         if user is None:
#             error = 'Invalid username'
#         elif not check_password_hash(user['pw_hash'],
#                                      request.form['password']):
#             error = 'Invalid password'
#         else:
#             flash('You were logged in')
#             session['user_id'] = user['user_id']
#             return redirect(url_for('timeline'))
#     return render_template('login.html', error=error)

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