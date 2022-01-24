# reviewDAO.py
#
# 작성일 : 2022. 01. 08
#
# 최종 수정 : 2022. 01. 08
#
# 게시판 댓글 작성과 표시를 위한 DAO 클래스 정의
# 기존 boardDAO 클래스들에 상속해서 사용할 것
#
###################################

import db_connection as dbc

dbc = dbc.db_conn()

class ReviewDAO:

    @classmethod
    def insertReview(cls, nickname,board_code, content, kind, id, ref) -> 'ReviewDAO':
        sql = "insert into review " \
              "values ('" + nickname + "',NULL, '" + id + "', '" + content + "', now()," + board_code + ", '" + kind + "'," + ref + ");"
        return dbc.execute(sql)

    @classmethod
    def selectReview(cls, board_code, kind) -> 'ReviewDAO':
        sql = "select r.* " \
              "from review r" \
              "where r.rv_board_num = " + board_code + " " \
              "and r.rv_board_kind = '" + kind + "';"
        return dbc.select(sql)

    @classmethod
    def deleteReviewCascade(cls, board_code, kind) -> 'ReviewDAO':
        sql = "delete from review where rv_board_num = " + board_code + " and rv_board_kind = '" + kind + "';"
        return dbc.execute(sql)

    @classmethod
    def deleteReview(cls, rv_num) -> 'ReviewDAO':
        sql = "delete from review where rv_num = " + rv_num + ";"
        return dbc.execute(sql)

    @classmethod
    def selectreivewPage(cls, reviewpage, limit, board_code, kind) -> 'ReviewDAO':
        sql = "select r.* from  review r "\
              "where r.rv_board_num = " + board_code + " " \
              "and r.rv_board_kind = '" + kind + "' " \
              "and r.rv_ref is null "\
              "order by r.rv_num asc LIMIT " + str((reviewpage - 1) * limit) + "," + str(limit) + ";"
        return dbc.select(sql)

    @classmethod
    def selectReviewcount(cls, board_code, kind) -> 'ReviewDAO':
        sql = "select count(*) " \
              "from review r,users u " \
              "where r.rv_board_num = " + board_code + " " \
              "and r.rv_board_kind = '" + kind + "' " \
              "and r.rv_ref is null "\
              "and u.usr_id = r.rv_author;"
        return dbc.select(sql)

    @classmethod
    def selectRefReview(cls, rev_num) -> 'ReviewDAO':
        sql = "select r.* " \
              "from review r " \
              "where r.rv_ref =" + rev_num + ";"
        return dbc.select(sql)


    @classmethod
    def selectRefPageReview(cls,ref_page,limit,rev_num) -> 'ReviewDAO':
        sql = "select r.* " \
              "from review r " \
              "where r.rv_ref =" + rev_num + \
              " LIMIT " + str((ref_page - 1) * limit) + "," + str(limit) + ";"
        return dbc.select(sql)

    @classmethod
    def selectRefReviewCount(cls, rev_num) -> 'ReviewDAO':
        sql = "select count(*) " \
              "from review r " \
              "where r.rv_ref =" + rev_num + ";"
        return dbc.select(sql)
