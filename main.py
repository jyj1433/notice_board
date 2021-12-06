# main.py
#
# 작성일 : 2021. 11. 20
# 최종 수정 : 2021. 12. 06
#
#
###################################

from flask import Flask, render_template

import db_connection as dbc

dbc = dbc.db_conn()

#Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = '플래쉬'

# 블루프린트 코드
from webapp.board import board_view
from webapp.login import login_view

app.register_blueprint(board_view.bp)
app.register_blueprint(login_view.bp)



@app.route('/') # 접속하는 url
def index():
    #return 'main'
    return render_template('index.html', title="index")




if __name__=="__main__":
    # app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)