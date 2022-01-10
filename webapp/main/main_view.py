from flask import Blueprint, render_template, request, send_file
import config
import webapp.main.mainDAO as mainDAO
import os
import modules.review.review_view as review_view

bp = Blueprint("main", __name__, url_prefix='/')
dao = mainDAO.MainDAO
config = config.host

# 초기화면
@bp.route('/')
def index():
    re = dao.selectBoardAll()
    return render_template('index.html', title="index", result=re)

# 게시글 상세보기
@bp.route("/main_get", methods=['GET'])
def main_get():
    board_code = request.args.get('idx')
    caption = request.args.get('caption')

    if caption == "자유게시판":
        review = review_view.review_pagenation(board_code,'b02')
        re = dao.selectBoardDetailFree(board_code)
        return render_template('board_free/board_free_result.html', result=re, title="게시판", page=1, reviewpage=review, idx=board_code, kind=".board_free_get")

    elif caption == "개발일지":
        review = review_view.review_pagenation(board_code,'b03')
        re = dao.selectBoardDetailDev(board_code)
        return render_template('board_dev/board_dev_result.html', result=re, title="게시판", page=1,  reviewpage=review, idx=board_code, kind=".board_dev_get")


@bp.route('/filetest',methods=['GET', 'POST']) # 파일업로드 테스트 페이지
def filetest():
    if request.method == 'POST':
        f = request.files['file']
        f.save('upload/'+ f.filename)
        return render_template('index.html', title="index")
    return render_template('fileTest.html', title="파일테스트")

@bp.route('/fileDown', methods = ['GET', 'POST'])
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


