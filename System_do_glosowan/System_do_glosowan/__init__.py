from flask import Flask
app = Flask(__name__)

from System_do_glosowan import views
from System_do_glosowan import fun_base
from System_do_glosowan import fun
from System_do_glosowan import fun_mail
from System_do_glosowan import message

app.run(debug=True)