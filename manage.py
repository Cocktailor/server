'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from flask import Flask
from flask import render_template;
from flask.ext.script import (Manager, Server)

from cocktailor.app import create_app
from cocktailor.extensions import db
from cocktailor.configs.default import DefaultConfig as Config
from cocktailor.utils.populate import create_test_data
app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("localhost", port=4418))

@manager.command
def createall(dropdb=False, createdb=False):
    """Creates the database with some testing content.
    If you do not want to drop or create the db add
    '-c' (to not create the db) and '-d' (to not drop the db)
    """
    
    db.drop_all()
    db.create_all()
    create_test_data()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    print("aaa??")
    error = None
    return render_template('login.html', error=error)

if __name__ == "__main__":
    manager.run()