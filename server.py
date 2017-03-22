from flask import *
from flask_bootstrap import Bootstrap
import os
import label_image

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
        select = request.form['photo_type']
        print(id, select)
        VkPhotos = label_image.photos_class(id)
        print(VkPhotos)
        return render_template('found.html', photos=VkPhotos[select], error=error, result='')
    return render_template('about.html', error=error, result='')


app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)