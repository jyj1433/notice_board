from flask import Blueprint, render_template, request, redirect, flash, session, escape
import webapp.member.memberDAO as memberDAO
import modules.review.review_view as review_view

bp = Blueprint("member", __name__, url_prefix='/')
dao = memberDAO.MemberDAO

# 회원가입
@bp.route('/join',methods=['GET','POST'])
def join_post():
    error = None
    error_id = None
    error_email = None
    error_nickname = None
    error_pw_com = None

    if request.method == 'POST':
        id = request.form['usr_id']
        pw = request.form['usr_pw']
        pw_com = request.form['usr_pw_com']
        email = request.form['usr_email']
        nickname = request.form['usr_nick']
        if id == '':
            error_id = "아이디를 입력하세요"
        elif pw == '':
            error = "비밀번호를 입력하세요"
        elif pw_com == '':
            error_pw_com = "비밀번호 확인을 입력하세요"
        elif pw != pw_com:
            error = "입력한 비밀번호와 확인이 다릅니다"
        elif email == '':
            error_email = "이메일을 입력하세요"
        elif nickname == '':
            error_nickname = "닉네임을 입력하세요"
        else:
            usr_id = dao.selectUserIdEmailNcikname()
            for idx in usr_id:
                if idx[0] == id:
                    error_id = "아이디가 중복되었습니다."
                elif idx[1] == email:
                    error_email = "이메일이 중복되었습니다."
                elif idx[2] == nickname:
                    error_nickname = "닉네임이 중복되었습니다."

        if error == None and error_id == None and error_email == None and error_pw_com == None and error_nickname == None:
            memberlist = [id, pw, email, nickname, ""]
            dao.insertMember(memberlist)
            flash("회원가입 성공")
            return redirect('/')
    return render_template('member/join.html', title="회원가입",
                           error=error, error_id=error_id,
                           error_email=error_email, error_nickname=error_nickname,
                           error_pw_com=error_pw_com)

# 로그인
@bp.route('/login',methods=['GET','POST'])
def login_post():
    error = None
    if request.method == 'POST':
        id = request.form['usr_id']
        pw = request.form['usr_pw']
        login_check = dao.selectLogin(id, pw)
        if id == '':
            error = '아이디를 입력해주세요.'
        elif not login_check:
            error = '아이디 또는 비밀번호가 일치하지 않습니다.'
        else:
            session['check'] = True
            session['id'] = id
            return redirect('/')
    return render_template('member/login.html', title="로그인", error=error)

# 로그아웃
@bp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect('/')

# 회원수정
@bp.route('/member_modify',methods=['GET','POST'])
def member_modify():
    error = None
    id = '%s' % escape(session['id'])
    result = dao.selectMember(id)

    if request.method == 'POST':
        pw = request.form['usr_pw']
        pw_com = request.form['usr_pw_com']
        name = request.form['usr_name']
        email = request.form['usr_email']

        if pw == '':
            error = "비밀번호를 입력하세요"
        elif pw != pw_com:
            error = "비밀번호가 다릅니다."

        if error == None :
            dao.updateMember(id, pw, email, name)
            flash("회원정보가 수정되었습니다.")
            return redirect('/')
    return render_template('member/member_modify.html', title="회원수정", result=result, error=error)

# 회원탈퇴
@bp.route('/member_delete',methods=['GET', 'POST'])
def member_delete():
    if request.method == 'POST':
        id = '%s' % escape(session['id'])
        pw = request.form['usr_pw']
        info = dao.selectMypageInfo(id)
        if pw == info[0][1]:
            dao.deleteMember(id)
            session.clear()
            flash("탈퇴되었습니다.")
            return render_template('member/login.html', title="index")
        else:
            flash("비밀번호가 틀렸습니다.")
            return render_template('member/member_delete.html', title="회원탈퇴")
    return render_template('member/member_delete.html', title="회원탈퇴")

# 아이디 비밀번호 찾기
@bp.route('/find_id_pw',methods=['GET', 'POST'])
def find_id_pw():
    error = None
    if request.method == 'POST':
        email = request.form.get('usr_email')
        re = dao.selectUserForEmail(email)
        if email == '':
            error = "이메일을 입력하세요"
        elif not re:
            error = "가입되지 않은 이메일입니다."

        if error == None :
            find = re[0][0]
            return render_template('member/find_id_pw.html', title="id/pw찾기", find=find)
        return render_template('member/find_id_pw.html', title="id/pw찾기", error=error)
    return render_template('member/find_id_pw.html', title="id/pw찾기")

# 마이페이지
@bp.route('/mypage',methods=['GET', 'POST'])
def mypage():
    id = '%s' % escape(session['id'])
    result = dao.selectMypagePost(id)
    reviews = dao.selectMypageReviews(id)
    info = dao.selectMypageInfo(id)
    return render_template('member/mypage.html', title="마이페이지", result=result, info=info, reviews=reviews)

# 마이페이지 최신글 상세보기
@bp.route("/mypage_get", methods=['GET'])
def mypage_get():
    board_code = request.args.get('idx')
    caption = request.args.get('caption')

    if caption == "자유게시판":
        review = review_view.review_pagenation(board_code, 'b02')
        re = dao.selectBoardDetailFree(board_code)
        return render_template('board_free/board_free_result.html', result=re, title="게시판", page=1, reviewpage=review, idx=board_code, kind=".board_free_get")
    elif caption == "개발일지":
        review = review_view.review_pagenation(board_code, 'b03')
        re = dao.selectBoardDetailDev(board_code)
        return render_template('board_dev/board_dev_result.html', result=re, title="게시판", page=1,  reviewpage=review, idx=board_code, kind=".board_dev_get")

# 마이페이지 프로필 이미지 업로드
@bp.route('/upload_prof_img', methods=['GET', 'POST'])
def upload_prof_img():
    if request.method == 'POST':
        if request.files['prof_img'].filename != '':    # 파일 첨부를 했을 경우
            id = request.form['id'] # hidden input으로 가져온 값 - 접속한 유저의 아이디 # session[id]로 가져오면 다른 ip에서 접속했을 때 이미지 못바꿈
            url = request.form['url'] # hidden input으로 가져온 값 - 접속한 유저의 ip
            f = request.files['prof_img']
            file_path = 'image/upload/prof_img/' + f.filename  # 이미지가 저장될 경로
            f.save('static/' + file_path)  # 이미지를 서버 디렉터리에 저장
            dao.updateProfImg(id, file_path) # db의 유저정보에 프로필 이미지 경로 추가
            flash("이미지 등록이 완료되었습니다.")
        else:
            url = request.form['url']  # hidden input으로 가져온 값 - 접속한 유저의 ip
            flash("등록된 이미지가 없습니다.")
        return redirect(url)