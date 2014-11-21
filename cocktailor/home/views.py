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

@home.route("/", methods=['GET'])
def index():
    orders = Order.query.all()
    OrdersArray = []
    for o in orders:
        OrdersArray = [o.values()] + OrdersArray
        
    return render_template("home/index.html", orders=OrdersArray)

@home.route("/<int:o_id>/done", methods=['GET','POST'])
def done(o_id):
    orders = Order.query.all()
    for o in orders:
        if o_id == o.id:
            o.change_status()
            o.save()
            break
    return redirect(url_for('home.index'))

@home.route("/getorder", methods=['POST'])
def getorder():
    table = request.form['table']
    price = request.form['price']
    order_content = request.form['order_content']
    time = request.form['time']
    o = Order()
    o.insert_table(table)
    o.insert_content(order_content)
    o.insert_time(time)
    o.insert_status()
    o.save()
    return "", 200

