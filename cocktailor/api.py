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

import threading
import time
import copy
import os
import json


api = Blueprint("api", __name__)


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

class WaitThread(threading.Thread):
    def run(self):
        print 'wait for 4 sec.....'
        global blesignal
        time.sleep(10)
        
        customer_ble_id = self._Thread__kwargs['customer_ble_id']
        blesignal_local = copy.deepcopy(blesignal[customer_ble_id])    
         
        blesignal_local.sort(reverse=True)
        print blesignal_local
        waiterinfo = blesignal_local[0]
        strength , waiter_device_id = waiterinfo
        print '\n total'
        print strength
#         user = User.query.filter_by(device_id=waiter_device_id).first()
#         waiter_reg_id = user.reg_id
#          
#         user = User.query.filter_by(ble_id=customer_ble_id).first()
#         table = user.table
#  
#         send_gcm_waiter(waiter_reg_id, table)

def send_gcm(waiter_reg_id, customer_ble_id):
    gcm = GCM('AIzaSyBsDGUDh_5O5O-BqipGljNLQMurQNRgP2M')
    data = {'ble_id': customer_ble_id}
    reg_id = waiter_reg_id
    gcm.plaintext_request(registration_id=reg_id, data=data)

def send_gcm_waiter(waiter_reg_id, table):
    gcm = GCM('AIzaSyBsDGUDh_5O5O-BqipGljNLQMurQNRgP2M')
    data = {'table': table}
    reg_id = waiter_reg_id
    gcm.plaintext_request(registration_id=reg_id, data=data)


@api.route('/register_user', methods=['POST'])
def register_user():
    device_id = request.form['device_id']
    reg_id = request.form['reg_id']
    iswaiter = request.form['iswaiter']
    waiter_name = request.form['waiter_name']

    print 'device_id(' + device_id + ') reg_id(' + reg_id + ') waiter(' + iswaiter + ')' 
    
    user = User.query.filter_by(device_id=device_id).first()
    if user is None:
        user = User()
    
    if len(device_id) != 0 :
        user.device_id = device_id
    if len(reg_id)  != 0 :
        user.reg_id = reg_id
    if len(iswaiter) != 0 :
        user.iswaiter = iswaiter
    user.save()
    
    return "", 200  

@api.route('/call_waiter', methods=['POST'])
def call_waiter():
    ble_id = request.form['ble_id']
    table = request.form['table']

    print ' ------------11111 call waiter ----------'
    print 'ble_id(' + ble_id + ') table(' + table + ')'
    
    wc = WC.query.filter_by(ble_id=ble_id).first()
    if wc is None:
        wc = WC()
    
    if len(ble_id) != 0 :
        wc.ble_id = ble_id
    if len(table)  != 0 :
        wc.table = table
    wc.save()

    count = User.query.filter_by(iswaiter='Y').count()
    print 'seng gcm to ', count,' client waiters'
    waiters = User.query.filter_by(iswaiter='Y')
    blesignal[ble_id] = []

    thread = WaitThread(kwargs={'customer_ble_id': ble_id})
    thread.start()

    for waiter in waiters :
        send_gcm(waiter.reg_id, ble_id)
    
    return "", 200

@api.route('/ble_signal', methods=['POST'])
def ble_signal():
    strength = request.form['strength']
    device_id = request.form['device_id']
    customer_ble_id = request.form['response_ble_id']
    
    wc = WC.query.filter_by(ble_id=customer_ble_id).first()
    if wc.device_id is None:
        wc.device_id = device_id
        wc.save()
    else:
        tmp_wc = WC()
        tmp_wc.ble_id = wc.ble_id
        tmp_wc.table = wc.table
        tmp_wc.device_id = device_id
        tmp_wc.save()

    print '\n-----------kkkkkk ble_signal ----------'
    print 'strength(' + strength + ') device_id(' + device_id + ') customer_ble_id(' + customer_ble_id +')'
    
    blesignal[customer_ble_id].append((int(strength), device_id))
    print blesignal
    
    return "", 200