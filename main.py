# main.py
#
# 작성일 : 2021. 11. 20
# 최종 수정 : 2021. 12. 30
#
# 프로그램 시작점
# 블루프린트 레지스터 관리
#
###################################
from flask import Flask, render_template, request
import requests
from datetime import datetime
import config
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'secretkey'

# 블루프린트 코드
from webapp.board import board_view
from webapp.member import member_view
from webapp.board_dev import board_dev_view
from webapp.board_free import board_free_view
from webapp.main import main_view
from modules.review import review_view
from webapp.admin import admin_view
from webapp.playground import playground_view


app.register_blueprint(board_view.bp)
app.register_blueprint(member_view.bp)
app.register_blueprint(board_dev_view.bp)
app.register_blueprint(board_free_view.bp)
app.register_blueprint(main_view.bp)
app.register_blueprint(review_view.bp)
app.register_blueprint(admin_view.bp)
app.register_blueprint(playground_view.bp)

def format_datetime(value):
    date = datetime.now()

    resurt = date - value
    if(resurt.days != 0):
        return 3600

    return resurt.seconds/60

def nowdate(r):
    return datetime.date(datetime.now())

def setConfig(r):
    return config.host

# jinja 환경변수 - html 어디에서나 사용 가능
app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['nowdate'] = nowdate
app.jinja_env.filters['ref_rev'] = review_view.ref_review
app.jinja_env.filters['admin'] = setConfig



if __name__=="__main__":
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)