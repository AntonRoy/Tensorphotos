from flask import *
from flask_bootstrap import Bootstrap
import os
import vkpars

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def start():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('main'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        id = request.form['login']
        photos = vkpars.user_photos(id)
        return render_template('found.html', photos=photos['my_photos'], photos1=photos['friends_photos'], photos2=photos['ff_photos'], error=error, result='')

    return render_template('about.html', error=error, result='')


app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)