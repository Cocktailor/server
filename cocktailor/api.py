'''
Created on 2014. 11. 28.

@author: hnamkoong
'''

from flask import Blueprint, send_file
from flask.globals import request
from cocktailor.auth.models import (User)
from cocktailor.menu.models import (Category, Menu)
from gcm import *
from multiprocessing import Process
import threading
import time
import os
import json


api = Blueprint("api", __name__)

blesignal = {}

@api.route('/menu_receive', methods=['GET'])
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

class WaitThread(threading.Thread):
    def run(self):
        print 'wait for 4 sec.....'
        global blesignal
        time.sleep(4)
        
        blesignal_local = blesignal
        customer_ble_id = self._Thread__kwargs['customer_ble_id']
        
         
        blesignal_local[customer_ble_id].sort(reverse=True)
        print blesignal_local[customer_ble_id]
        waiterinfo = blesignal_local[customer_ble_id][0]
        strength , waiter_device_id = waiterinfo
        print '\n total'
        print strength
        user = User.query.filter_by(device_id=waiter_device_id).first()
        waiter_reg_id = user.reg_id
         
        user = User.query.filter_by(ble_id=customer_ble_id).first()
        table = user.table
 
        send_gcm_waiter(waiter_reg_id, table)
        
        


@api.route('/call_waiter', methods=['POST'])
def call_waiter():
    ble_id = request.form['ble_id']
    table = request.form['table']

    print ' ------------11111 call waiter ----------'
    print 'ble_id(' + ble_id + ') table(' + table + ')'
    
    user = User.query.filter_by(ble_id=ble_id).first()
    if user is None:
        user = User()
    
    if len(ble_id) != 0 :
        user.ble_id = ble_id
    if len(table)  != 0 :
        user.table = table
    user.save()
    

    count = User.query.filter_by(iswaiter='Y').count()
    print 'seng gcm to ' + repr(count) + ' clients'
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

    print '\n-----------kkkkkk ble_signal ----------'
    print 'strength(' + strength + ') device_id(' + device_id + ') customer_ble_id(' + customer_ble_id +')'
    
    blesignal[customer_ble_id].append((int(strength), device_id))
    print blesignal
    
    return "", 200
    
    