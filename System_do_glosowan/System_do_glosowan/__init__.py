from flask import Flask
app = Flask(__name__)

import views
import fun_base
import fun
import fun_mail
import message

app.run(debug=True)