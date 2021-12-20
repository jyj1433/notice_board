from flask import Flask, Blueprint, render_template, request, redirect, flash,session
import math
import webapp.board.boardDAO as boardDAO

bp = Blueprint("board", __name__, url_prefix='/')
dao = boardDAO.BoardDAO

# 게시글 상세보기
@bp.route("/get", methods=['GET'])
def get():
    board_code = request.args.get('idx')
    page = request.args.get('page')
    re = dao.selectBoardDetail(board_code)
    return render_template('board/board_result.html', result=re, title="게시판",page=page)

# 게시판 목록
@bp.route('/board', methods=['GET'])
def board():

    search = request.args.get('search')
    page = request.args.get('page', type=int, default=1)    # 페이지
    limit = 5  #보여지는 게시글 갯수
    re = dao.selectBoardPage(page, limit)

    full = dao.selectBoardCount()   # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기
    tot_count = full[0][0]

    last_page_num = math.ceil(tot_count / limit)    # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)

    return render_template('board/board.html', result=re, title="게시판", search=search,
        datas=re,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count)

# 글쓰기 페이지
@bp.route('/board_write', methods=['GET', 'POST'])
def board_write():
    error = None

    if session.get('check') != True:
        flash("로그인 해주세요")
        return redirect("/board")
    if request.method == 'POST':
        title = request.form['b_title']
        content = request.form['b_content']
        author = session.get('id')
        if title == '':
            error = "제목을 입력해주세요"
        elif content == '':
            error = "내용을 입력해주세요"
        else:
            dao.insertBoard(title, content, author)
            flash("글이 작성되었습니다.")
            return redirect('/board')
        flash(error)
    return render_template('board/board_write.html', title="글쓰기")

# 게시글 삭제하기
@bp.route("/delete", methods=['GET'])
def delete():

    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    page = request.args.get('page')
    if session.get('id') != re[0][4]:
        flash("글 작성자 만이 삭제가능합니다.")
        return redirect('/get?idx='+board_code +'&page=' + page)
    dao.deleteBoard(board_code)
    flash("글이 삭제되었습니다")
    return redirect('/board')

# 게시글 수정하기
@bp.route("/modify", methods=['GET','POST'])
def modify():
    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    page = request.args.get('page')
    if session.get('id') != re[0][4]:
        flash("글 작성자 만이 수정가능합니다.")
        return redirect('/get?idx='+board_code +'&page=' + page)
    if request.method == 'POST':
        title = request.form['b_title']
        content = request.form['b_content']
        author = request.form['b_author']
        if title == '':
            error = "제목을 입력해주세요"
        elif author == '' :
            error = "작성자를 입력해주세여"
        elif content == '':
            error = "내용을 입력해주세요"
        else:
            dao.updateBoard(board_code,title, content)
            flash("글이 수정되었습니다.")
            return redirect('/board')
        return error
    return render_template('board/board_modify.html', title="글쓰기", result=re)

# 게시판 목록
@bp.route('/board_search', methods=['GET'])
def board_search():
    search = request.args.get('search')

    page = request.args.get('page', type=int, default=1)    # 페이지
    limit = 5  #보여지는 게시글 갯수
    re = dao.selectBoardSearchPage(page, limit, search)

    full = dao.selectBoardSearchCount(search)   # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기
    tot_count = full[0][0]

    last_page_num = math.ceil(tot_count / limit)    # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)

    return render_template('board/board.html', result=re, title="게시판", search=search,
        datas=re,
        limit=limit,
        page=page,
        block_start=block_start,
        block_end=block_end,
        last_page_num=last_page_num,
        tot_count=tot_count)