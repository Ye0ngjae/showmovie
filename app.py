from flask import *
import os
from movie import *

app = Flask(__name__)

movie = {
    'num': '',
    'title': '',
    'stat': '',
    'info': ''
}

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
        num = get_num(url)
        print(get_title(num))
        print(get_movie_stat(num))
        print(get_movie_info(num))
        
        
        return render_template('request.html')

if __name__ == '__main__':
    app.run(debug=True)