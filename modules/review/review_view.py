from flask import Blueprint, render_template, request, redirect, flash, session
import modules.review.reviewDAO as reviewDAO

bp = Blueprint("review", __name__, url_prefix='/')
dao = reviewDAO.ReviewDAO

# 댓글 쓰기
@bp.route("/review_write", methods=['GET', 'POST'])
def review_write():
    # get으로 가져온 값들
    board_code = request.args.get('idx') # 게시글의 기본키
    page = request.args.get('page') # 현재 페이지
    id = session.get('id') # 로그인된 아이디

    # post로 가져온 값들
    kind = request.form.get('kind')  # 게시판 종류
    review_content = request.form.get('review_content')  # 댓글 내용

    if session.get('check') != True:
        flash("로그인 해주세요")

        if kind == 'b01':
            return redirect('/get?idx=' + board_code + '&page=' + page)
        elif kind == 'b02':
            return redirect('/board_free_get?idx=' + board_code + '&page=' + page)
        elif kind == 'b03':
            return redirect('/board_dev_get?idx=' + board_code + '&page=' + page)

    # 로그인이 되어있을 경우 - 댓글 작성 성공
    dao.insertReview(board_code, review_content, kind, id)
    if kind == 'b01':
        return redirect('/get?idx=' + board_code + '&page=' + page)
    elif kind == 'b02':
        return redirect('/board_free_get?idx=' + board_code + '&page=' + page)
    elif kind == 'b03':
        return redirect('/board_dev_get?idx=' + board_code + '&page=' + page)

