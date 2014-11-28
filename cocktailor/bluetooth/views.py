'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint
from flask.globals import request
from cocktailor.auth.models import User
from gcm import *

import threading
import time
import copy

ble = Blueprint("ble", __name__)

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


@ble.route('/register_user', methods=['POST'])
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

@ble.route('/call_waiter', methods=['POST'])
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
    print 'seng gcm to ', count,' client waiters'
    waiters = User.query.filter_by(iswaiter='Y')
    blesignal[ble_id] = []

    thread = WaitThread(kwargs={'customer_ble_id': ble_id})
    thread.start()

    for waiter in waiters :
        send_gcm(waiter.reg_id, ble_id)
    
    return "", 200

@ble.route('/ble_signal', methods=['POST'])
def ble_signal():
    strength = request.form['strength']
    device_id = request.form['device_id']
    customer_ble_id = request.form['response_ble_id']

    print '\n-----------kkkkkk ble_signal ----------'
    print 'strength(' + strength + ') device_id(' + device_id + ') customer_ble_id(' + customer_ble_id +')'
    
    blesignal[customer_ble_id].append((int(strength), device_id))
    print blesignal
    
    return "", 200
    
    