'''
Created on 2014. 11. 17.

@author: hnamkoong
'''

from flask import Blueprint, flash, redirect, url_for, request, current_app
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from cocktailor.auth.forms import LoginForm
from cocktailor.auth.models import User
from cocktailor.menu.models import Category,Menu
from cocktailor.extensions import db
from cocktailor.utils.helpers import render_template

menu = Blueprint("menu", __name__)

@menu.route("/", methods=['GET', 'POST'])
def index():
    categories = Category.query.all()
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())
    menus = Menu.query.all()
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    return render_template("menu/index.html", categories=CategoriesArray, menus=MenusArray)

@menu.route("/edit", methods=['GET', 'POST'])
def edit():
    categories = Category.query.all()
    CategoriesArray = []
    for c in categories:
        CategoriesArray.append(c.values())
    menus = Menu.query.all()
    MenusArray = []
    for m in menus:
        MenusArray.append(m.values())
        
    return render_template("menu/edit.html", categories=CategoriesArray, menus=MenusArray)

@menu.route("/edit/new_category", methods=["POST", "GET"])
def new_category():
    if request.method == "POST":
        name = request.form['cname']
        desc = request.form['cdesc']
        ctgr = Category()
        ctgr.insert_name(name)
        ctgr.insert_description(desc)
        ctgr.save()
        return redirect(url_for('menu.edit'))
    return render_template("menu/new_category.html")

@menu.route("/edit/<int:c_id>/new_menu", methods=["POST", "GET"])
def new_menu(c_id):
    if request.method == "POST":
        name = request.form['mname']
        desc = request.form['mdesc']
        price = request.form['mprice']
        menu = Menu()
        menu.insert_name(name)
        menu.insert_price(price)
        menu.insert_description(desc)
        menu.insert_category_id(c_id)
        menu.save()
        return redirect(url_for('menu.edit'))
    return render_template("menu/new_menu.html")

@menu.route("/edit/<int:c_id>/del_category", methods=["POST", "GET"])
def del_category(c_id):
    categories = Category.query.all()
    menus = Menu.query.all()
    for m in menus:
        if m.category_id == c_id:
            m.delete()
    for c in categories:
        if c.id == c_id:
            c.delete()
            break
    return redirect(url_for('menu.edit'))

@menu.route("/edit/<int:m_id>/del_menu", methods=["POST", "GET"])
def del_menu(m_id):
    menus = Menu.query.all()
    for m in menus:
        if m.id == m_id:
            m.delete()
            break
    return redirect(url_for('menu.edit'))

