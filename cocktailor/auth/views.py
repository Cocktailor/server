'''
Created on 2014. 11. 16.

@author: hnamkoong
'''

from flask import Blueprint, flash, redirect, url_for, request, current_app

from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from cocktailor.auth.forms import LoginForm
from cocktailor.auth.models import User
from cocktailor.utils.helpers import render_template

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                                form.password.data)

        if user and authenticated:
#             login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or
                            url_for("home.index"))
            
        flash(("Wrong username or password"), "danger")

    return render_template("auth/login.html", form=form)

# class RegistrationForm(Form):
#     username = TextField('Username', [validators.Length(min=4, max=25)])
#     email = TextField('Email Address', [validators.Length(min=6, max=35)])
#     password = PasswordField('New Password', [
#         validators.Required(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the TOS', [validators.Required()])
    
from flask import Flask
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import (DataRequired, Email, EqualTo, regexp,
                                ValidationError)
from werkzeug import secure_filename

import os
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

import string
import random
def id_generator(size=80, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@auth.route("/fileupload", methods=["GET", "POST"])
def fileupload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        extention = '.' in filename and filename.rsplit('.', 1)[1]
        if file and (extention in ALLOWED_EXTENSIONS) :
            random_filename = id_generator() + '.' + extention
            filename = secure_filename(random_filename)
            app = Flask("cocktailor")
            path = os.path.join(app.config['PICTURE_STORE_PATH'], filename)
            file.save(path)
            return '55'
    return render_template("test/fileupload.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(("Logged out"), "success")
    return redirect(url_for("auth.login"))













