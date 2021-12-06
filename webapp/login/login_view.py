from flask import Flask, Blueprint, render_template, request, redirect, flash

import math
import db_connection as dbc

bp = Blueprint("login", __name__, url_prefix='/')
dbc = dbc.db_conn()

@bp.route('/join',methods=['GET','POST']) # 회원가입 페이지
def join_post():
    error = None
    error_id = None
    if request.method == 'POST':
        id = request.form['usr_id']
        pw = request.form['usr_pw']
        pw_com = request.form['usr_pw_com']
        email = request.form['usr_email']
        nickname = request.form['usr_nick']
        if pw == '':
            error = "비밀번호를 입력하세요"
        elif pw != pw_com:
            error = "비밀번호가 다릅니다."
        if id == '':
            error_id = "아이디를 입력하세요"
        else:
            sql = 'select usr_id from users;'
            usr_id = dbc.select(sql)
            for idx in usr_id:
                if idx[0] == id:
                    error_id = "아이디가 중복되었습니다."

        if error == None and error_id == None:
            sql = "insert into users values('" + id + "', '" + pw + "', '" + email + "', '" + nickname + "')"
            dbc.execute(sql)
            flash("회원가입 성공")
            return redirect('/')

    return render_template('login/join.html', title="회원가입", error=error, error_id=error_id)
