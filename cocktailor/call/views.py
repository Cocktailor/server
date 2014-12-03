'''
Created on 2014. 11. 29.

@author: hnamkoong
'''

from flask import Blueprint, request, redirect, url_for
from flask_login import current_user
from cocktailor.extensions import db
from cocktailor.call.models import WaiterCall as Call
from cocktailor.call.models import FunctionalCallName as FCN
from cocktailor.utils.helpers import render_template, make_file

call = Blueprint("call", __name__)

@call.route("/", methods=['GET'])
def index():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    calls = Call.query.filter_by(restaurant_id = current_user.restaurant_id)
    CallsArray = []
    for c in calls:
        CallsArray.append(c.values())
        
    return render_template("call/index.html", calls=CallsArray)

@call.route("/callcount", methods=['POST'])
def callcount():
    callCount = Call.query.filter_by(restaurant_id = current_user.restaurant_id).count()
    return str(callCount), 200

@call.route("/view_call", methods=['GET'])
def view_call():
    if not (current_user is not None and current_user.is_authenticated()):
        return redirect(url_for('auth.login'))
    fcns = FCN.query.filter_by(restaurant_id = current_user.restaurant_id)
    Fcns = []
    for f in fcns:
        Fcns.append(f.values())
    return render_template("call/view.html", fcns = Fcns)

@call.route("/view_call/new_call", methods=["POST", "GET"])
def new_call():
    if request.method == "POST":
        name = request.form['fcname']
        img = request.files['fcfile']
        fcn = FCN()
        fcn.insert_name(name)
        fcn.insert_restaurant_id(current_user.restaurant_id)
        if img:
            filename = make_file(img)
            fcn.insert_picture(filename)
        fcn.save()
        return redirect(url_for('call.view_call'))
    return render_template("call/new_call.html")

@call.route("/view_call/<int:f_id>/del_call", methods=["POST", "GET"])
def del_call(f_id):
    FCN.query.filter_by(id=f_id).delete()
    db.session.commit()
    return redirect(url_for('call.view_call'))