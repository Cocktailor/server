'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint, flash, redirect, url_for, request, current_app
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from cocktailor.auth.forms import LoginForm
from cocktailor.auth.models import User
from cocktailor.menu.models import Category,Menu
from cocktailor.extensions import db
from cocktailor.utils.helpers import render_template

menu = Blueprint("menu", __name__)

@menu.route("/", methods=['GET', 'POST'])
def index():
    categories = Category.query.all()
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())
    menus = Menu.query.all()
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    return render_template("menu/index.html", categories=CategoriesArray, menus=MenusArray)