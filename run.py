from flask import Flask
from flask import render_template, flash, redirect, url_for, request, session
import numpy as np


app = Flask(__name__)


@app.route('/')
@app.route('/')
@app.route('/strona_startowa')
def strona_startowa():
    return render_template('strona_startowa.html')


if __name__ == '__main__':
    app.run()