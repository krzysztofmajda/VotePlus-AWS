"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import views
import fun_base
import fun
import fun_mail
import message

app.secret_key = fun.random_string(50)