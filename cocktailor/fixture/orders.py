'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from collections import OrderedDict

fixture = [
    {
        'user_id' : 1,
        'order_content' : "Daiquiri X 1 / Mojito X 2", 
        'price' : 40,
        'table' : 1,
        'status' : 'pending'
    },
    {
        'user_id' : 1,
        'order_content' : "Mojito X 1", 
        'price' : 40,
        'table' : 3,
        'status' : 'pending'
    },
    {
        'user_id' : 1,
        'order_content' : "Hurricane X 2", 
        'price' : 40,
        'table' : 8,
        'status' : 'pending'
    },
    {
        'user_id' : 1,
        'order_content' : "Daiquiri X 1 / Hurricane X 2 / Mojito X 2", 
        'price' : 40,
        'table' : 2,
        'status' : 'pending'
    },
    {
        'user_id' : 1,
        'order_content' : "Daiquiri X 1 / Mojito X 2", 
        'price' : 40,
        'table' : 4,
        'status' : 'pending'
    },
    {
        'user_id' : 1,
        'order_content' : "Daiquiri X 1 / Hurricane X 2 / Mojito X 2", 
        'price' : 40,
        'table' : 2,
        'status' : 'done'
    },
    {
        'user_id' : 1,
        'order_content' : "Daiquiri X 1 / Mojito X 2", 
        'price' : 40,
        'table' : 4,
        'status' : 'done'
    },
]