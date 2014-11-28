'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint, redirect, url_for, request

from cocktailor.home.models import Order
from cocktailor.utils.helpers import render_template
from flask_login import current_user

home = Blueprint("home", __name__)

@home.route("/", methods=['GET'])
def index():
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
    o.insert_price(price)
    o.insert_time(time)
    o.insert_status()
    o.insert_restaurant_id(current_user.restaurant_id)
    o.save()
    return "", 200

