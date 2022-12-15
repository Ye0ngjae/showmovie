from flask import *
import os
import shutil
from movie import *
import sqlite3

#os.remove('movie.db')
#shutil.rmtree('static/img/movie', ignore_errors=True)

conn = sqlite3.connect('movie.db', check_same_thread=False, isolation_level=None)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS movie \
    (id INTEGER PRIMARY KEY AUTOINCREMENT, num text, title text, date text, info text)") #Database 생성

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    if(c.execute("SELECT * FROM movie").fetchall() == []): #데이터가 없을 경우
        status = 0
    else: #데이터가 있을 경우
        status = 1
    
    row = c.execute("SELECT * FROM movie").fetchall() #데이터베이스에서 데이터 가져오기
    
    return render_template('list.html',status=status, rows=row) #list.html에 데이터 전달

@app.route('/request', methods=['GET', 'POST']) #GET, POST 방식 모두 사용
def request_page():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        try:
            url = request.form['url']
            if(url == '' or 'https://movie.naver.com/movie/bi/mi/basic.naver?code=' not in url): #입력값 검증
                return "<script>alert('잘못된 형식의 입력입니다.');history.back();</script>" #오류 발생시 이전 페이지로 이동
        
            num = get_num(url) #영화 번호 가져오기
            title = get_title(num) #영화 제목 가져오기
            date = get_date(num) #영화 개봉일 가져오기
            info = get_info(num) #영화 정보 가져오기

            if(c.execute("SELECT * FROM movie WHERE num = ?", (num,)).fetchone() == None): #중복 검증
                c.execute("INSERT INTO movie (num, title, date, info) VALUES (?, ?, ?, ?)", (num, title, date, info)) #데이터베이스에 추가
            else:
                return "<script>alert('이미 존재하는 영화입니다.');history.back();</script>" #중복시 이전 페이지로 이동
        
            return render_template('request.html')
        except:
            return "<script>alert('오류가 발생했습니다.');history.back()</script>" #오류 발생시 이전 페이지로 이동
    
@app.route('/movie/<int:num>')
def movie(num):
    try:
        row = c.execute("SELECT * FROM movie WHERE num = ?", (num,)).fetchall() #데이터베이스에서 데이터 가져오기
    
        return render_template('movie.html', rows=row) #movie.html에 데이터 전달
    except:
        return "<script>alert('오류가 발생했습니다.');history.back()</script>" #오류 발생시 이전 페이지로 이동

if __name__ == '__main__':
    app.run(debug=True)