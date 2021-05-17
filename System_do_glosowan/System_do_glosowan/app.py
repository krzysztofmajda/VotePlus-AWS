"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from app import System_do_glosowan.views
from app import System_do_glosowan.fun_base
from app import System_do_glosowan.fun
from app import System_do_glosowan.fun_mail
from app import System_do_glosowan.message

app.secret_key = fun.random_string(50)