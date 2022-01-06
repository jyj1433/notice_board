from flask import Blueprint, render_template, request, redirect, flash, session
import math
import config
import webapp.board_free.board_freeDAO as board_freeDAO

bp = Blueprint("board_free", __name__, url_prefix='/')
dao = board_freeDAO.Board_freeDAO

# 게시글 상세보기
@bp.route("/board_free_get", methods=['GET'])
def board_free_get():
    board_code = request.args.get('idx')
    page = request.args.get('page')
    re = dao.selectBoardDetail(board_code)
    return render_template('board_free/board_free_result.html', result=re, title="게시판",page=page)

# 게시판 목록
@bp.route('/board_free')
def board_free():
    search_keyword = request.args.get('search', type=str, default="") # 검색어
    search_option = request.args.get('search_select', type=str, default="opt_all")    # 검색옵션
    page = request.args.get('page', type=int, default=1)    # 페이지
    limit = 5  #보여지는 게시글 갯수

    if search_keyword == "":
        re = dao.selectBoardPage(page, limit)
        full = dao.selectBoardCount()  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기
    else:
        if search_option == "opt_title":
            option = "bf_title"
        elif search_option == "opt_author":
            option = "bf_author"
        else:
            option = "concat(bf_title, bf_author)"

        re = dao.selectBoardSearchPage(page, limit, search_keyword, option)
        full = dao.selectBoardSearchCount(search_keyword, option)  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기

    tot_count = full[0][0]
    last_page_num = math.ceil(tot_count / limit)    # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)

    title = "게시판 " + str(page) + "p"

    return render_template('board_free/board_free.html', result=re, title=title, search=search_keyword, opt=search_option,
        datas=re,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count)

# 글쓰기 페이지
@bp.route('/board_free_write', methods=['GET', 'POST'])
def board_free_write():
    error = None
    if session.get('check') != True:
        flash("로그인 해주세요")
        return redirect("/board_free")
    if request.method == 'POST':
        title = request.form['bf_title']
        content = request.form['bf_content']
        author = session.get('id')
        if title == '':
            error = "제목을 입력해주세요"
        elif content == '':
            error = "내용을 입력해주세요"
        else:
            dao.insertBoard(title, content, author)
            flash("글이 작성되었습니다.")
            return redirect('/board_free')
        flash(error)
    return render_template('board_free/board_free_write.html', title="글쓰기" , config = config.host)

# 게시글 삭제하기
@bp.route("/board_free_delete", methods=['GET'])
def board_free_delete():
    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    page = request.args.get('page')
    if session.get('id') != re[0][5]:
        flash("글 작성자 만이 삭제가능합니다.")
        return redirect('/board_free_get?idx='+board_code +'&page=' + page)
    dao.deleteBoard(board_code)
    flash("글이 삭제되었습니다")
    return redirect('/board_free')

# 게시글 수정하기
@bp.route("/board_free_modify", methods=['GET','POST'])
def board_free_modify():
    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    page = request.args.get('page')

    if session.get('id') != re[0][5]:
        flash("글 작성자 만이 수정가능합니다.")
        return redirect('/board_free_get?idx='+board_code+'&page=' + page)
    if request.method == 'POST':
        title = request.form['bf_title']
        content = request.form['bf_content']
        author = request.form['bf_author']
        if title == '':
            error = "제목을 입력해주세요"
        elif author == '':
            error = "작성자를 입력해주세여"
        elif content == '':
            error = "내용을 입력해주세요"
        else:
            dao.updateBoard(board_code,title, content)
            flash("글이 수정되었습니다.")
            return redirect('/board_free_get?idx='+board_code+'&page='+page)
        return error
    return render_template('board_free/board_free_modify.html', title="글쓰기", result=re,page=page)


# 댓글 쓰기
@bp.route("/board_free_review_write", methods=['GET', 'POST'])
def board_free_review_write():
    # get으로 가져온 값들
    board_code = request.args.get('idx') # 게시글의 기본키
    page = request.args.get('page') # 현재 페이지
    id = session.get('id')

    if session.get('check') != True:
        flash("로그인 해주세요")
        return redirect('/board_free_get?idx='+board_code+'&page=' + page)

    # post로 가져온 값들
    kind = request.form.get('kind') # 게시판 종류
    review_content = request.form.get('review_content') # 댓글 내용

    dao.insertReview(board_code, review_content, kind, id)

    return redirect('/board_free_get?idx='+board_code+'&page='+page)



