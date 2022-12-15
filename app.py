from flask import *
import os
from movie import *
import sqlite3

conn = sqlite3.connect('movie.db', check_same_thread=False, isolation_level=None)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS movie \
    (id INTEGER PRIMARY KEY AUTOINCREMENT, num text, title text, date text, info text)")

app = Flask(__name__)

def get_list():
    sql = '''SELECT title, date, info FROM movie'''


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    if(c.execute("SELECT * FROM movie").fetchall() == []):
        status = 0
    else:
        status = 1
    
    row = c.execute("SELECT * FROM movie").fetchall()
    
    return render_template('list.html',status=status, rows=row)

@app.route('/request', methods=['GET', 'POST'])
def request_page():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        try:
            url = request.form['url']
            if(url == '' or 'https://movie.naver.com/movie/bi/mi/basic.naver?code=' not in url): #입력값 검증
                return "<script>alert('잘못된 형식의 입력입니다.');history.back();</script>"
        
            num = get_num(url)
            title = get_title(num)
            date = get_date(num)
            info = get_info(num)

            if(c.execute("SELECT * FROM movie WHERE num = ?", (num,)).fetchone() == None):
                c.execute("INSERT INTO movie (num, title, date, info) VALUES (?, ?, ?, ?)", (num, title, date, info))
            else:
                return "<script>alert('이미 존재하는 영화입니다.');history.back();</script>"
        
            return render_template('request.html')
        except:
            return "<script>alert('오류가 발생했습니다.');history.back()</script>"
    
@app.route('/movie/<int:num>')
def movie(num):
    try:
        row = c.execute("SELECT * FROM movie WHERE num = ?", (num,)).fetchall()
    
        return render_template('movie.html', rows=row)
    except:
        return "<script>alert('오류가 발생했습니다.');history.back()</script>"

if __name__ == '__main__':
    app.run(debug=True)