from flask import Flask, Blueprint, render_template, request, redirect, flash, session, escape
import webapp.member.memberDAO as memberDAO

bp = Blueprint("member", __name__, url_prefix='/')
dao = memberDAO.MemberDAO

# 회원가입 페이지
@bp.route('/join',methods=['GET','POST'])
def join_post():
    error = None
    error_id = None
    if request.method == 'POST':
        id = request.form['usr_id']
        pw = request.form['usr_pw']
        pw_com = request.form['usr_pw_com']
        email = request.form['usr_email']
        nickname = request.form['usr_nick']
        if pw == '':
            error = "비밀번호를 입력하세요"
        elif pw != pw_com:
            error = "비밀번호가 다릅니다."
        if id == '':
            error_id = "아이디를 입력하세요"
        else:
            usr_id = dao.selectUserId()
            for idx in usr_id:
                if idx[0] == id:
                    error_id = "아이디가 중복되었습니다."

        if error == None and error_id == None:
            memberlist = [id, pw, email, nickname]
            dao.insertMember(memberlist)
            flash("회원가입 성공")
            return redirect('/')
    return render_template('member/join.html', title="회원가입", error=error, error_id=error_id)

# 로그인 페이지
@bp.route('/login',methods=['GET','POST'])
def login_post():
    if request.method == 'POST':
        id = request.form['usr_id']
        pw = request.form['usr_pw']
        login_check = dao.selectLogin(id, pw)
        if not login_check:
            flash("아이디 또는 비밀번호가 틀렸습니다.")
            return redirect('/login')
        else:
            session['check'] = True
            session['id'] = id
            return redirect('/')
    return render_template('member/login.html', title="로그인")

@bp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect('/')

#마이페이지(미완성->비밀번호 확인 유효성 검사)
@bp.route('/member_modify',methods=['GET','POST'])
def member_modify():
    id = '%s' % escape(session['id'])
    result = dao.selectMember(id)

    if request.method == 'POST':
        pw = request.form['usr_pw']
        name = request.form['usr_name']
        email = request.form['usr_email']
        dao.updateMember(id, pw, email, name)
        flash("회원정보가 수정되었습니다.")
        return redirect('/')
    else:
        return render_template('member/member_modify.html', title="마이페이지", result=result)
    return render_template('member/member_modify.html', title="마이페이지", result=result)