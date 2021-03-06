from flask import Blueprint, render_template, request, redirect, flash, session
import math
import config
import webapp.board.boardDAO as boardDAO
import modules.review.review_view as review_view
import webapp.common.commonDAO as commonDAO
from modules import replace_image

bp = Blueprint("board", __name__, url_prefix='/')
dao = boardDAO.BoardDAO
commonDAO = commonDAO.CommonDAO
config = config.host

# 게시글 상세보기
@bp.route("/get", methods=['GET'])
def get():
    board_code = request.args.get('idx')
    page = request.args.get('page')
    list_value = []
    list_test= [["list|kind"],["list2|kind"],["List|app"]]
    list_kind_value = []
    list_app_value = []
    for x in list_test:
        list_value.append(x[0].split("|"))
    for x in list_value:
        if(x[1] == "kind"):
            list_kind_value.append(x[0])
        else:
            list_app_value.append(x[0])
    re = dao.selectBoardDetail(board_code)
    re = replace_image.replace(re)
    review = review_view.review_pagenation(board_code, 'b01')
    return render_template('board/board_result.html', result=re, title="게시판", page=page, config=config,reviewpage=review,idx=board_code, kind=".get")

# 게시판 목록
@bp.route('/board')
def board():
    search_keyword = request.args.get('search', type=str, default="") # 검색어
    search_option = request.args.get('search_select', type=str, default="opt_all")    # 검색옵션
    page = request.args.get('page', type=int, default=1)    # 페이지
    limit = 5  #보여지는 게시글 갯수

    if search_keyword == "":
        re = dao.selectBoardPage(page, limit)
        full = dao.selectBoardCount()  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기
    else:
        if search_option == "opt_title":
            option = "b_title"
        elif search_option == "opt_author":
            option = "b_nickname"
        else:
            option = "concat(b_title, b_nickname)"

        re = dao.selectBoardSearchPage(page, limit, search_keyword, option)
        full = dao.selectBoardSearchCount(search_keyword, option)  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기

    tot_count = full[0][0]
    last_page_num = math.ceil(tot_count / limit)    # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    title = "게시판 " + str(page) + "p"
    return render_template('board/board.html', result=re, title=title, search=search_keyword, opt=search_option,
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
    id = session.get('id')
    if session.get('check') != True:
        flash("로그인 해주세요")
        return redirect("/board")

    try:
        if request.method == 'POST':
            nickname = commonDAO.selectNickname(id)
            title = request.form['b_title']
            content = request.form['b_content']
            content = content.replace(config,"{{config}}")
            author = request.form['id']
            if title == '':
                error = "제목을 입력해주세요"
            elif content == '':
                error = "내용을 입력해주세요"
            elif request.files['b_file'].filename != '':
                file = request.files['b_file']
                file_name = 'upload/' + file.filename
                dao.insertBoardfile(nickname, title, content, author, file_name)
                flash("글이 작성되었습니다.")
                return redirect('/board')
            else:
                dao.insertBoard(nickname, title, content, author)
                flash("글이 작성되었습니다.")
                return redirect('/board')
            flash(error)
        return render_template('board/board_write.html', title="글쓰기", config=config, id=id)
    except:
        flash("글자 수 제한을 넘었습니다")

# 게시글 삭제하기
@bp.route("/delete", methods=['GET'])
def delete():
    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    page = request.args.get('page')

    if session.get('id') != re[0][5] and session.get('id') != "root":
        flash("글 작성자 만이 삭제가능합니다.")
        return redirect('/get?idx='+board_code +'&page=' + page)
    elif re[0][5] == None and session.get('id') != "root":
        flash("글 작성자 만이 삭제가능합니다.")
        return redirect('/get?idx=' + board_code + '&page=' + page)

    dao.deleteBoard(board_code)
    dao.deleteReviewCascade(board_code, 'b01')
    flash("글이 삭제되었습니다")
    return redirect('/board')

# 게시글 수정하기
@bp.route("/modify", methods=['GET','POST'])
def modify():
    board_code = request.args.get('idx')
    re = dao.selectBoardDetail(board_code)
    re =replace_image.replace(re)
    page = request.args.get('page')

    if session.get('id') != re[0][5] or re[0][5] == None:
        flash("글 작성자 만이 수정가능합니다.")
        return redirect('/get?idx='+board_code +'&page=' + page)

    if request.method == 'POST':
        title = request.form['b_title']
        content = request.form['b_content']
        content = content.replace(config.host, "{{config}}")
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
            return redirect('/get?idx='+board_code+'&page='+page)
        return error
    return render_template('board/board_modify.html', title="글쓰기", result=re, page=page,config=config)
