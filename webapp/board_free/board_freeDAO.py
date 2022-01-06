import db_connection as dbc

dbc = dbc.db_conn()

class Board_freeDAO:

    @classmethod
    def selectBoardList(cls) -> 'Board_freeDAO':
        sql = "select * from board_free"
        return dbc.select(sql)

    @classmethod
    def selectBoardCount(cls) -> 'Board_freeDAO':
        sql = "select count(*) from board_free"
        return dbc.select(sql)

    @classmethod
    def selectBoardPage(cls, page, limit) -> 'Board_freeDAO':
        sql = 'select users.usr_name as nickname, board_free.* from board_free, users where board_free.bf_author = users.usr_id order by bf_num desc LIMIT ' + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetail(cls, board_code) -> 'Board_freeDAO':
        sql = 'select users.usr_name as nickname, board_free.* from board_free, users where board_free.bf_author = users.usr_id and board_free.bf_num = ' + board_code + ';'
        return dbc.select(sql)

    @classmethod
    def insertBoard(cls, title, content, author) -> 'Board_freeDAO':
        sql = "insert into board_free values (NULL,'" + title + "', date_format(now(),'%Y-%m-%d') ,'" + content + "','" + author + "', now(), 'b02');"
        dbc.execute(sql)

    @classmethod
    def deleteBoard(cls, board_code) -> 'Board_freeDAO':
        sql = 'delete from board_free where bf_num = ' + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def updateBoard(cls, board_code, title, content) -> 'Board_freeDAO':
        sql = "update board_free " \
              "set bf_title = '" + title + "', bf_content = '" + content + "' where bf_num = " + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def selectBoardSearchCount(cls, keyword, option) -> 'Board_freeDAO':
        sql = "select count(*) " \
              "from board_free " \
              "where " + option + " like '%" + keyword + "%';"
        return dbc.select(sql)

    @classmethod
    def selectBoardSearchPage(cls, page, limit, keyword, option) -> 'Board_freeDAO':
        sql = "select users.usr_name as nickname, board_free.* " \
              "from board_free, users " \
              "where board_free.bf_author = users.usr_id and " + option + " like '%" + keyword + "%' order by bf_num desc LIMIT " + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def insertReview(cls, board_code, content, kind, id) -> 'Board_freeDAO':
        sql = "insert into review values (NULL, '" + id + "', '" + content + "', now()," + board_code + ", '" + kind + "');"
        return dbc.execute(sql)