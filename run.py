from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/')
@app.route('/strona_startowa')
def strona_startowa():
    if 'log_in_user_id' in session or 'activate_user_id' in session:
        loged_in = True
    else:
        loged_in = False
    return render_template('strona_startowa.html', info=message.main_page(), loged_in=loged_in)


if __name__ == '__main__':
    app.run()