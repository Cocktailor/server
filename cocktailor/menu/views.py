'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint,redirect, url_for, request

from flask.ext.login import current_user

from cocktailor.menu.models import Category,Menu
from cocktailor.extensions import db
from cocktailor.utils.helpers import render_template, id_generator
from cocktailor.configs.default import DefaultConfig as Config

from werkzeug import secure_filename

import os

menu = Blueprint("menu", __name__)

@menu.route("/", methods=['GET', 'POST'])
def index():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    categories = Category.query.filter_by(restaurant_id=current_user.restaurant_id)
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())
    menus = Menu.query.filter_by(restaurant_id=current_user.restaurant_id)
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    return render_template("menu/index.html", categories=CategoriesArray, menus=MenusArray)

@menu.route("/edit/", methods=['GET', 'POST'])
def edit():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    categories = Category.query.filter_by(restaurant_id=current_user.restaurant_id)
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())
    menus = Menu.query.filter_by(restaurant_id=current_user.restaurant_id)
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    return render_template("menu/edit.html", categories=CategoriesArray, menus=MenusArray)

@menu.route("/<string:c_name>/<int:m_id>", methods=["GET"])
def view_menu(c_name, m_id):
    m = Menu.query.filter_by(id=m_id).first()
    return render_template("menu/menu.html",menu=m)

@menu.route("/edit/new_category", methods=["POST", "GET"])
def new_category():
    if request.method == "POST":
        name = request.form['cname']
        desc = request.form['cdesc']
        ctgr = Category()
        ctgr.insert_name(name)
        ctgr.insert_description(desc)
        ctgr.insert_restaurant_id(current_user.restaurant_id)
        ctgr.save()
        return redirect(url_for('menu.edit'))
    return render_template("menu/new_category.html")

@menu.route("/edit/<int:c_id>/new_menu", methods=["POST", "GET"])
def new_menu(c_id):
    if request.method == "POST":
        name = request.form['mname']
        desc = request.form['mdesc']
        price = request.form['mprice']
        file = request.files['mfile']
        filename = file.filename
        extention = '.' in filename and filename.rsplit('.', 1)[1]
        menu = Menu()
        menu.insert_name(name)
        menu.insert_price(price)
        menu.insert_description(desc)
        menu.insert_category_id(c_id)
        menu.insert_restaurant_id(current_user.restaurant_id)
        if file and (extention in Config.ALLOWED_EXTENSIONS) :
            random_filename = id_generator() + '.' + extention
            filename = secure_filename(random_filename)
            path = os.path.join(Config.PICTURE_STORE_PATH, filename)
            file.save(path)
            menu.insert_picture(filename)
        menu.save()
        return redirect(url_for('menu.edit'))
    return render_template("menu/new_menu.html")

@menu.route("/edit/<int:c_id>/del_category", methods=["POST", "GET"])
def del_category(c_id):
    Menu.query.filter_by(category_id=c_id).delete()
    Category.query.filter_by(id=c_id).delete()
    db.session.commit()
    return redirect(url_for('menu.edit'))

@menu.route("/edit/<int:m_id>/del_menu", methods=["POST", "GET"])
def del_menu(m_id):
    Menu.query.filter_by(id=m_id).delete()
    db.session.commit()
    return redirect(url_for('menu.edit'))

