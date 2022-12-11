from flask import *
import os
import movie

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        url = request.form['url']
        print(url)
        num = movie.get_num(url)
        title = movie.get_title(num)
        info = movie.get_movie_info(num)
        stat = movie.get_movie_stat(num)
        print(title)
        print(stat)
        print(info)
        return render_template('request.html')

if __name__ == '__main__':
    app.run(debug=True)