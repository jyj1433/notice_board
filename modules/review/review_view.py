import math

from flask import Blueprint, render_template, request, redirect, flash, session
import modules.review.reviewDAO as reviewDAO
import modules.nickname_select as nickname_select

bp = Blueprint("review", __name__, url_prefix='/')
dao = reviewDAO.ReviewDAO

# 댓글 쓰기
@bp.route("/review_write", methods=['GET', 'POST'])
def review_write():
    # get으로 가져온 값들
    board_code = request.args.get('idx') # 게시글의 기본키
    page = request.args.get('page') # 현재 페이지
    id = session.get('id') # 로그인된 아이디
    review_page = request.args.get('reviewpage')

    if review_page == '0':
        review_page = '1'


    # post로 가져온 값들
    kind = request.form.get('kind')  # 게시판 종류
    review_content = request.form.get('review_content')  # 댓글 내용
    review_ref = request.form.get('ref_review') # 대댓글추가


    if session.get('check') != True:
        flash("로그인 해주세요")

        if kind == 'b01':
            return redirect('/get?idx=' + board_code + '&page=' + page)
        elif kind == 'b02':
            return redirect('/board_free_get?idx=' + board_code + '&page=' + page)
        elif kind == 'b03':
            return redirect('/board_dev_get?idx=' + board_code + '&page=' + page)

    # 로그인이 되어있을 경우 - 댓글 작성 성공
    nickname = nickname_select.selectNickname(id)
    dao.insertReview(nickname, board_code, review_content, kind, id, review_ref)
    if kind == 'b01':
        return redirect('/get?idx=' + board_code + '&page=' + page + '&reviewpage=' + review_page)
    elif kind == 'b02':
        return redirect('/board_free_get?idx=' + board_code + '&page=' + page + '&reviewpage=' + review_page)
    elif kind == 'b03':
        return redirect('/board_dev_get?idx=' + board_code + '&page=' + page + '&reviewpage=' + review_page)

# 댓글 삭제
@bp.route("/review_delete", methods=['GET', 'POST'])
def review_delete():
    rv_num = request.args.get('rv_num')
    current_url = request.args.get('cur_url')
    page = request.args.get('page')
    current_url = current_url+'&page='+page

    dao.deleteReview(rv_num)
    return redirect(current_url)

def review_pagenation(board_code,kind):
    reviewpage = request.args.get('reviewpage', type=int, default=1)  # 페이지
    limit = 5  # 보여지는 댓글 갯수

    re = dao.selectreivewPage(reviewpage, limit, board_code, kind)
    full = dao.selectReviewcount(board_code, kind)  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기

    tot_count = full[0][0]
    last_page_num = math.ceil(tot_count / limit)  # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((reviewpage - 1) / block_size)  # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    review_page =[reviewpage,limit,re,tot_count,last_page_num,block_size,block_num,block_start,block_end]
    return review_page

def ref_review(rev_num):
    ref_rev = dao.selectRefReview(str(rev_num))
    ref_len = len(ref_rev)
    ref_list = [ref_rev,ref_len]
    return ref_list


