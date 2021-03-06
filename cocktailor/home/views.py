'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint, redirect, url_for, Request
# from flask import Response
from flask_login import current_user
from cocktailor.home.models import Order
from cocktailor.utils.helpers import render_template

from datetime import datetime
# from itertools import count

home = Blueprint("home", __name__)

@home.route("/", methods=['GET'])
def index():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    orders = Order.query.filter_by(restaurant_id = current_user.restaurant_id)
    OrdersArray = []
    for o in orders:
        OrdersArray = [o.values()] + OrdersArray
        
    return render_template("home/index.html", orders=OrdersArray)

@home.route("/<int:o_id>/done", methods=['GET','POST'])
def done(o_id):
    orders = Order.query.filter_by(restaurant_id = current_user.restaurant_id)
    for o in orders:
        if o_id == o.id:
            o.change_status(datetime.now().strftime("%m/%d %H:%M"))
            o.save()
            break
    return redirect(url_for('home.index'))

@home.route("/ordercount", methods=['POST'])
def ordercount():
    orderCount = Order.query.filter_by(restaurant_id = current_user.restaurant_id).count()
    return str(orderCount), 200
    