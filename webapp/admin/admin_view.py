from flask import Blueprint, render_template, request, flash, redirect
import webapp.admin.adminDAO as adminDAO
import math

bp = Blueprint("admin", __name__, url_prefix='/')
dao = adminDAO.AdminDAO

# 관리자 페이지
@bp.route('/admin', methods = ['GET', 'POST'])
def admin():

    dumped_board_list = dumped_board()

    search_keyword = request.args.get('search', type=str, default="")  # 검색어
    page = request.args.get('page', type=int, default=1) # 페이지
    limit = 5  # 보여지는 유저 수

    if search_keyword == "":
        members = dao.selectMemberAdmin(page, limit)
        full = dao.selectMemberCountAdmin()  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기
    else:
        members = dao.selectMemberSearchAdmin(page, limit, search_keyword)
        full = dao.selectMemberSearchCountAdmin(search_keyword)  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기

    tot_count = full[0][0]
    last_page_num = math.ceil(tot_count / limit)  # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)  # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)

    return render_template('admin/admin.html',
                           title="administrator",
                           members=members,
                           page=page,
                           search=search_keyword,
                           limit=limit,
                           block_start=block_start,
                           block_end=block_end,
                           last_page_num=last_page_num,
                           tot_count=tot_count,
                           dumped_board_list=dumped_board_list)

def dumped_board():
    page = request.args.get('dumped_board_page', type=int, default=1)  # 페이지
    limit = 5  # 보여지는 유저 수

    dumped_board = dao.selectBoardDumpedAdmin(page, limit)
    full = dao.selectCountBoardDumpedAdmin()  # 게시물의 총 개수 세기, 마지막 페이지의 수 구하기

    tot_count = full[0][0]
    last_page_num = math.ceil(tot_count / limit)  # 반드시 올림을 해줘야함

    block_size = 5  # 페이지 블럭을 5개씩 표기
    block_num = int((page - 1) / block_size)  # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_start = (block_size * block_num) + 1  # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_end = block_start + (block_size - 1)  # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)

    dumped_board_list = [page, limit, dumped_board, full, tot_count, last_page_num, block_size, block_num, block_start, block_end]

    return dumped_board_list


@bp.route('/del_member', methods = ['GET', 'POST'])
def del_member():

    check_list = request.form.getlist('check')
    if not check_list:
        flash("선택된 항목이 없습니다.")
    else:
        dao.deleteMemberAdmin(check_list)
        flash("처형되었습니다.")

    return redirect('/admin')


@bp.route('/del_dumped_board', methods = ['GET', 'POST'])
def del_dumped_board():
    check_list = request.form.getlist('check')

    if not check_list:
        flash("선택된 항목이 없습니다.")
    else:
        temp = []
        b01_list = []
        b02_list = []
        b03_list = []

        for i in check_list:
            temp.append(i.split(','))

        for i in temp:
            if i[1] == 'b01':
                b01_list.append(i[0])
            if i[1] == 'b02':
                b02_list.append(i[0])
            if i[1] == 'b03':
                b03_list.append(i[0])

        dao.deleteBoardDumpedAdmin(b01_list)
        dao.deleteBoard_freeDumpedAdmin(b02_list)
        dao.deleteBoard_devDumpedAdmin(b03_list)
        flash("처형되었습니다.")

    return redirect('/admin')
