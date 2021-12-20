# main.py
#
# 작성일 : 2021. 11. 20
# 최종 수정 : 2021. 12. 13
#
#
###################################
import os

from flask import Flask, render_template, request, send_file, jsonify

#Flask 객체 인스턴스 생성
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secretkey'

# 블루프린트 코드
from webapp.board import board_view
from webapp.member import member_view

app.register_blueprint(board_view.bp)
app.register_blueprint(member_view.bp)

@app.route('/') # 초기화면 render
def index():
    return render_template('index.html', title="index")


@app.route('/filetest',methods=['GET','POST']) # 파일업로드 테스트 페이지
def filetest():
    if request.method == 'POST':
        f = request.files['file']
        print(secure_filename(f.filename))
        f.save('upload/'+ secure_filename(f.filename))

        return render_template('index.html', title="index")
    return render_template('fileTest.html', title="파일테스트")

@app.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
    if request.method == 'POST':
        sw=0
        files = os.listdir("./upload")
        for x in files:
            if(x==request.form['file']):
                sw=1

        path = "./upload/"
        return send_file(path + request.form['file'],
                attachment_filename = request.form['file'],
                as_attachment=True)



if __name__=="__main__":
    # host 등을 직접 지정하고 싶다면
    app.run(host="0.0.0.0", port="5000", debug=True)