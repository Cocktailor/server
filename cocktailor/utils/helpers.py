'''
Created on 2014. 11. 16.

@author: hnamkoong
'''

from flask.ext.themes2 import render_theme_template

from cocktailor.configs.default import DefaultConfig as Config

from werkzeug import secure_filename

import string
import random
import os


def render_template(template, **context):
    """A helper function that uses the `render_theme_template` function
    without needing to edit all the views
    """
    
    return render_theme_template('bootstrap3', template, **context)

def id_generator(size=80, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_file(img_file):
    filename = img_file.filename
    extention = '.' in filename and filename.rsplit('.', 1)[1]
    if extention in Config.ALLOWED_EXTENSIONS:
        random_filename = id_generator() + '.' + extention
        filename = secure_filename(random_filename)
        path = os.path.join(Config.PICTURE_STORE_PATH, filename)
        img_file.save(path)
    return filename
        
