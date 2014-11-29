'''
Created on 2014. 11. 12.

@author: hnamkoong
'''

from cocktailor.menu.models import Category, Menu
from cocktailor.home.models import Order
from cocktailor.call.models import FunctionalCallName
  
def create_default_categories():
    from cocktailor.fixture.categories import fixture
    for data in fixture:
        category = Category()
        for k in data:
            v = data[k]
            setattr(category, k, v)
        category.save()
    

def create_default_menus():
    from cocktailor.fixture.menus import fixture
    for data in fixture:
        menu = Menu()
        for k in data:
            v = data[k]
            setattr(menu, k, v)
        menu.save()

def create_default_orders():
    from cocktailor.fixture.orders import fixture
    for data in fixture:
        order = Order()
        for k in data:
            v = data[k]
            setattr(order, k, v)
        order.save()
        
def create_default_functionalcallname():
    from cocktailor.fixture.functionalcallname import fixture
    for data in fixture:
        fcn = FunctionalCallName()
        for k in data:
            v = data[k]
            setattr(fcn, k, v)
        fcn.save()
    

def create_test_data():
    create_default_categories()
    create_default_menus()
    create_default_orders()
    create_default_functionalcallname()
