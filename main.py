import math

from flask import Flask, render_template , request
import board.db_connection as dbc

dbc = dbc.db_conn()

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    return render_template('index.html', title="index")


@app.route("/get", methods=['GET'])
def get():
    board_code = request.args.get('idx')
    sql = 'select * from board where b_num = ' + board_code + ";"
    re = dbc.select(sql)
    return render_template('board_result.html', result=re, title="게시판");

@app.route('/board') # 게시판 목록
def board():
    #sql = 'delete from board where b_num=2;'
    #dbc.delete(sql)
    page = request.args.get('page', type=int, default=1)  # 페이지
    limit = 10
    sql = 'select * from board LIMIT ' + str((page-1)*limit) +','+ str(limit) +';'
    re = dbc.select(sql)
    sql = 'select * from board'
    # 게시물의 총 개수 세기
    full = dbc.select(sql)
    tot_count = len(full)
    # 마지막 페이지의 수 구하기
    last_page_num = math.ceil(tot_count / limit)  # 반드시 올림을 해줘야함

    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    return render_template('board.html', result=re, title="게시판",
        datas=re,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num)

@app.route('/board_write') # 글쓰기 페이지
def board_write():
    return render_template('board_write.html', title="글쓰기")

@app.route('/join') # 회원가입 페이지
def join():
    return render_template('join.html', title="회원가입")

if __name__=="__main__":
    # app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)