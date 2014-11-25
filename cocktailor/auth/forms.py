'''
Created on 2014. 11. 16.

@author: hnamkoong
'''

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, regexp


USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=("You can only use letters, numbers or dashes"))

class LoginForm(Form):
    login = StringField("Username or E-Mail", validators=[
        DataRequired(message="You must provide an email adress or username")])

    password = PasswordField("Password", validators=[
        DataRequired(message="Password required")])

    remember_me = BooleanField("Remember Me", default=False)
