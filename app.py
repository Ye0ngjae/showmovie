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
        print(request.form.get('url'))
        

if __name__ == '__main__':
    app.run(debug=True)