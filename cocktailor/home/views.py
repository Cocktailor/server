'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint, flash, redirect, url_for, request, current_app
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from cocktailor.auth.forms import LoginForm
from cocktailor.auth.models import User
from cocktailor.home.models import Order
from cocktailor.extensions import db
from cocktailor.utils.helpers import render_template

home = Blueprint("home", __name__)

@home.route("/", methods=['GET', 'POST'])
def index():
    orders = Order.query.all()
    OrdersArray = []
    for o in orders:
        OrdersArray.append(o.values())
        
    return render_template("home/index.html", orders=OrdersArray)