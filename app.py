from flask import *
import os
from movie import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    print(movie)
    
    return render_template('list.html', movie=movie)

@app.route('/request', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        url = request.form['url']
        if(url == '' or 'https://movie.naver.com/movie/bi/mi/basic.naver?code=' not in url): #입력값 검증
            return "<script>alert('잘못된 형식의 입력입니다.');history.back();</script>"
        num = get_num(url)
        print(url)
        print(num)
        print(get_title(num))
        
        return render_template('request.html')
    
@app.route('/movie/<int:num>')
def movie(num):
    
    return render_template('movie.html', title='')

if __name__ == '__main__':
    app.run(debug=True)