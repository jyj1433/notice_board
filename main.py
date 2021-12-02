import pymysql
from flask import Flask, render_template , request
import board.db_connection as dbc

dbc = dbc.db_conn()

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    return render_template('index.html', title="index")

@app.route('/db') # db 가져와서 보여주기
def db():
    #sql = 'delete from board where b_num=2;'
    #dbc.delete(sql)

    sql = 'select * from board;'
    re = dbc.select(sql)
    return render_template('db.html', result=re, title="DB불러오기")

@app.route("/get", methods=['GET'])
def get():
    board_code = request.args.get('idx')
    sql = 'select * from board where b_num = ' + board_code + ";"
    re = dbc.select(sql)
    return render_template('board_result.html', result=re);

@app.route('/board') # db 가져와서 보여주기
def board():
    #sql = 'delete from board where b_num=2;'
    #dbc.delete(sql)

    sql = 'select * from board;'
    re = dbc.select(sql)
    return render_template('board.html', result=re, title="게시판")


@app.route('/join') # 회원가입 페이지
def join():
    return render_template('join.html', title="회원가입")

if __name__=="__main__":
    # app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)