'''
Created on 2014. 11. 28.

@author: hnamkoong
'''

from flask import Blueprint, send_file
from cocktailor.menu.models import Category, Menu
from cocktailor.configs.default import DefaultConfig as Config
from flask.globals import request
from cocktailor.auth.models import User
from cocktailor.call.models import WaiterCall as WC, FunctionalCallName
from cocktailor.home.models import Order
from gcm import *
from datetime import datetime

import threading
import time
import copy
import os
import json


api = Blueprint("api", __name__)

CallWaitTime = 6


@api.route('/picture/<string:fname>', methods=['GET'])
def picture_receive(fname):
    path = os.path.join(Config.PICTURE_STORE_PATH, fname)
    return send_file(path, mimetype='image/gif')

@api.route('/menu_receive/<int:r_id>', methods=['GET'])
def menu_receive(r_id):
    categories = Category.query.filter_by(restaurant_id=r_id)
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())

    menus = Menu.query.filter_by(restaurant_id=r_id)
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    fcns = FunctionalCallName.query.filter_by(restaurant_id=r_id)
    fcnArray = []
    for fnc in fcns:
        fcnArray.append(fnc.values())
        
    result = {}
    result['category'] = CategoriesArray
    result['menu'] = MenusArray
    result['functional_call_name'] = fcnArray
#     print(result)
    jsonString = json.dumps(result,sort_keys=True)
    return jsonString

@api.route("/getorder", methods=['POST'])
def getorder():
    table = request.form['table']
    price = request.form['price']
    order_content = request.form['order_content']
    time = request.form['time']
    restaurant_id = request.form['restaurant_id']
    
    print 'table(' + table + ') price(' + price + ') order_content(' + order_content + ') time(' +  time + ') restaurant_id(' + restaurant_id + ')'
    
    o = Order()
    o.insert_table(table)
    o.insert_content(order_content)
    o.insert_price(price)
    o.insert_time(time)
    o.insert_restaurant_id(restaurant_id)
    o.insert_status()
    o.save()
    return "", 200


blesignal = {}

def send_gcm(waiter_reg_id, customer_ble_id):
    gcm = GCM('AIzaSyBsDGUDh_5O5O-BqipGljNLQMurQNRgP2M')
    data = {'ble_id': customer_ble_id}
    reg_id = waiter_reg_id
    gcm.plaintext_request(registration_id=reg_id, data=data)

def send_gcm_waiter(waiter_reg_id, table, functional_call_name):
    gcm = GCM('AIzaSyBsDGUDh_5O5O-BqipGljNLQMurQNRgP2M')
    data = {'table': table, 'functional_call_name': functional_call_name}
    reg_id = waiter_reg_id
    gcm.plaintext_request(registration_id=reg_id, data=data)


@api.route('/register_user', methods=['POST'])
def register_user():
    device_id = request.form['device_id']
    reg_id = request.form['reg_id']
    iswaiter = request.form['iswaiter']
    waiter_name = request.form['waiter_name']
    restaurant_id = request.form['restaurant_id']

    print 'device_id(' + device_id + ') reg_id(' + reg_id + ') waiter(' + iswaiter + ') waiter_name(' +  waiter_name + ') restaurant_id(' + restaurant_id + ')'
    
    user = User.query.filter_by(device_id=device_id).first()
    if user is None:
        user = User()
    
    if len(device_id) != 0 :
        user.device_id = device_id
    if len(reg_id)  != 0 :
        user.reg_id = reg_id
    if len(iswaiter) != 0 :
        user.iswaiter = iswaiter
    if len(waiter_name) != 0 :
        user.waiter_name = waiter_name
    if len(restaurant_id) != 0 :
        user.restaurant_id = restaurant_id
    user.save()
    
    return "", 200

@api.route('/call_waiter', methods=['POST'])
def call_waiter():
    ble_id = request.form['ble_id']
    table = request.form['table']
    functional_call_name = request.form['functional_call_name']
    restaurant_id = request.form['restaurant_id']

    print ' ------------11111 call waiter ----------'
    print 'ble_id(' + ble_id + ') table(' + table + ') functional_call_name(' + functional_call_name + ') restaurant_id(' + restaurant_id + ')'
    
    blesignal[ble_id] = []
    
    count = User.query.filter_by(iswaiter='Y').count()
    
    if count == 0:
        return "", 200
    
    print 'seng gcm to ', count,' client waiters'
    waiters = User.query.filter_by(iswaiter='Y', restaurant_id=restaurant_id)
    for waiter in waiters :
        send_gcm(waiter.reg_id, ble_id)
    
    print 'Wait Thread. wait for ' + repr(CallWaitTime) + ' sec.....'
    time.sleep(CallWaitTime)

    blesignal_local = copy.deepcopy(blesignal[ble_id])
    
    if len(blesignal_local) == 0 :
        waiter = waiters.first()
        print 'no ble signal, randome choise name>' + waiter.waiter_name 
    else :
        blesignal_local.sort(reverse=True)
        print blesignal_local
        waiterinfo = blesignal_local[0]
        strength , waiter_device_id = waiterinfo
        print '\n total'
        print strength
        waiter = User.query.filter_by(device_id=waiter_device_id).first()
    

    send_gcm_waiter(waiter.reg_id, table, functional_call_name)

    wc = WC()
    wc.ble_id = ble_id
    wc.table = table
    wc.functional_call_name = functional_call_name
    wc.waiter_name = waiter.waiter_name
    wc.time = datetime.now().strftime("%m/%d %H:%M")
    wc.restaurant_id = restaurant_id
    wc.save()
    
    return "", 200

@api.route('/ble_signal', methods=['POST'])
def ble_signal():
    strength = request.form['strength']
    device_id = request.form['device_id']
    customer_ble_id = request.form['response_ble_id']
    
    st = int(strength)+100
    print '\n-----------kkkkkk ble_signal ----------'
    print 'strength(', st, ') device_id(' + device_id + ') customer_ble_id(' + customer_ble_id +')'
    
    blesignal[customer_ble_id].append((st, device_id))
    print blesignal
    
    return "", 200