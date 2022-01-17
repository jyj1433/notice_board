import db_connection as dbc

dbc = dbc.db_conn()

class MemberDAO:

    @classmethod
    def selectUserId(cls) -> 'MemberDAO':
        sql = 'select usr_id from users;'
        return dbc.select(sql)

    @classmethod
    def insertMember(cls, memberlist) -> 'MemberDAO':
        sql = "insert into users values %r;" % (tuple(memberlist),)
        return dbc.execute(sql)

    @classmethod
    def selectLogin(cls, id, pw) -> 'MemberDAO':
        sql = 'select usr_id ' \
              'from users ' \
              'where usr_id = "' + id + '" and usr_pw = "' + pw + '" ;'
        return dbc.select(sql)

    @classmethod
    def selectMember(cls, id) -> 'MemberDAO':
        sql = 'select * ' \
              'from users ' \
              'where usr_id = "' + id + '" ;'
        return dbc.select(sql)

    @classmethod
    def updateMember(cls, id, pw, email, name) -> 'MemberDAO':
        sql = 'update users ' \
              'set usr_pw = "' + pw + '", usr_email = "' + email + '", usr_name = "' + name + '" where usr_id = "' + id + '";'
        dbc.execute(sql)

    @classmethod
    def deleteMember(cls, id) -> 'MemberDAO':
        sql = 'delete from users where usr_id= "' + id + '";'
        dbc.execute(sql)

    @classmethod
    def selectUserForEmail(cls, email) -> 'MemberDAO':
        sql = 'select * from users where usr_email = "' + email + '";'
        return dbc.select(sql)

    # 마이페이지 내가 쓴 글 조회 - dev,free
    @classmethod
    def selectMypagePost(cls, id) -> 'MemberDAO':
        sql = '(select b.bd_num as num, b.bd_title as title, b.bd_datetime as dt, k.k_caption ' \
              'from board_dev b, kind_boards k ' \
              'where b.kind=k.k_code and b.bd_author = "' + id + '") ' \
              'union ' \
              '(select b.bf_num, b.bf_title, b.bf_datetime as dt, k.k_caption ' \
              'from board_free b, kind_boards k ' \
              'where b.kind=k.k_code and b.bf_author = "' + id + '") ' \
              'order by dt desc limit 0, 3;'
        return dbc.select(sql)

    # 마이페이지 내가 쓴 댓글 조회
    @classmethod
    def selectMypageReviews(cls, id) -> 'MemberDAO':
        sql = 'select k.k_caption, r.* ' \
              'from review r, kind_boards k ' \
              'where r.rv_author = "' + id + '" and k_code = r.rv_board_kind ' \
              'order by r.rv_datetime desc limit 0, 3;'
        return dbc.select(sql)

    # 마이페이지 유저 정보 조회
    @classmethod
    def selectMypageInfo(cls, id) -> 'MemberDAO':
        sql = 'select * ' \
              'from users ' \
              'where usr_id = "' + id + '" ;'
        return dbc.select(sql)

    # 상세보기 개발일지
    @classmethod
    def selectBoardDetailDev(cls, board_code) -> 'MemberDAO':
        sql = 'select board_dev.* ' \
              'from board_dev ' \
              'where board_dev.bd_num = ' + board_code + ';'
        return dbc.select(sql)

    # 상세보기 자유게시판
    @classmethod
    def selectBoardDetailFree(cls, board_code) -> 'MemberDAO':
        sql = 'select board_free.* ' \
              'from board_free ' \
              'where board_free.bf_num = ' + board_code + ';'
        return dbc.select(sql)

    # 마이페이지 프로필 이미지 등록
    @classmethod
    def updateProfImg(cls, id, filePath) -> 'MemberDAO':
        sql = "update users " \
              "set usr_img = '" + filePath + "' " \
              "where usr_id = '" + id + "' ;"
        return dbc.execute(sql)