# main.py
#
# 작성일 : 2021. 11. 20
# 최종 수정 : 2021. 12. 30
#
# 프로그램 시작점
# 블루프린트 레지스터 관리
#
###################################
from flask import Flask, render_template

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey'

# 블루프린트 코드
from webapp.board import board_view
from webapp.member import member_view
from webapp.board_dev import board_dev_view
from webapp.board_free import board_free_view
from webapp.main import main_view
from modules.review import review_view


app.register_blueprint(board_view.bp)
app.register_blueprint(member_view.bp)
app.register_blueprint(board_dev_view.bp)
app.register_blueprint(board_free_view.bp)
app.register_blueprint(main_view.bp)
app.register_blueprint(review_view.bp)

def format_datetime(value):
    date = datetime.now()
    resurt = date - value
    return resurt.seconds/60

app.jinja_env.filters['datetime'] = format_datetime




@app.route('/rockcut')
def rockcut():
    return render_template('rockcut.html', title="index")

if __name__=="__main__":
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)