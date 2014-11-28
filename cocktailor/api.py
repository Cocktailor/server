'''
Created on 2014. 11. 28.

@author: hnamkoong
'''

from flask import Blueprint, send_file
from cocktailor.menu.models import Category, Menu
from cocktailor.configs.default import DefaultConfig as Config
import os
import json


api = Blueprint("api", __name__)

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
        
    result = {}
    result['category'] = CategoriesArray
    result['menu'] = MenusArray
#     print(result)
    jsonString = json.dumps(result,sort_keys=True)
    return jsonString

@api.route('/picture/<string:fname>', methods=['GET'])
def picture_receive(fname):
    path = os.path.join(Config.PICTURE_STORE_PATH, fname)
    return send_file(path, mimetype='image/gif')

