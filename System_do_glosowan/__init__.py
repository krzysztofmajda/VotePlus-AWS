"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import System_do_glosowan.views
import System_do_glosowan.fun_base
import System_do_glosowan.fun
import System_do_glosowan.fun_mail
import System_do_glosowan.message

#app.secret_key = fun.random_string(50)
