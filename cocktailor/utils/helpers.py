'''
Created on 2014. 11. 16.

@author: hnamkoong
'''

from flask.ext.themes2 import render_theme_template

import string
import random


def render_template(template, **context):
    """A helper function that uses the `render_theme_template` function
    without needing to edit all the views
    """
    
    return render_theme_template('bootstrap3', template, **context)

def id_generator(size=80, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
