'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from cocktailor.extensions import db
from cocktailor.bluetooth.views import send_gcm_waiter,blesignal
from cocktailor.auth.models import User

import threading
import time
import copy

class WaitThread(threading.Thread):
    def run(self):
        print 'wait for 4 sec.....'
#         global blesignal
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