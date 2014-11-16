'''
Created on 2014. 11. 16.

@author: hnamkoong
'''

from flask import Blueprint, flash, redirect, url_for, request, current_app
auth = Blueprint("auth", __name__)

from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from cocktailor.auth.forms import LoginForm
from cocktailor.auth.models import User
from cocktailor.utils.helpers import render_template

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                                form.password.data)

        print(user)
        print(authenticated)
        
#         if user and authenticated:
#             login_user(user, remember=form.remember_me.data)
#             return redirect(request.args.get("next") or
#                             url_for("forum.index"))
#         flash(("Wrong username or password"), "danger")

    return render_template("auth/login.html", form=form)