from flask import Blueprint, render_template, request
import config
import webapp.main.mainDAO as mainDAO

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
        re = dao.selectBoardDetailFree(board_code)
        return render_template('board_free/board_free_result.html', result=re, title="게시판", page=1)

    elif caption == "개발일지":
        re = dao.selectBoardDetailDev(board_code)
        return render_template('board_dev/board_dev_result.html', result=re, title="게시판", page=1)