import db_connection as dbc

dbc = dbc.db_conn()

class BoardDAO:

    @classmethod
    def selectBoardList(cls) -> 'BoardDAO':
        sql = "select * from board"
        return dbc.select(sql)

    @classmethod
    def selectBoardCount(cls) -> 'BoardDAO':
        sql = "select count(*) from board"
        return dbc.select(sql)

    @classmethod
    def selectBoardPage(cls, page, limit) -> 'BoardDAO':
        sql = 'select * from board order by b_num desc LIMIT ' + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetail(cls, board_code) -> 'BoardDAO':
        sql = 'select * from board where b_num = ' + board_code + ";"
        return dbc.select(sql)

    @classmethod
    def insertBoard(cls, title, content, author) -> 'BoardDAO':
        sql = "insert into board values (NULL,'" + title + "', date_format(now(),'%Y-%m-%d') ,'" + content + "','" + author + "', NULL);"
        dbc.execute(sql)

    @classmethod
    def insertBoardfile(cls, title, content, author, file_name) -> 'BoardDAO':
        sql = "insert into board values (NULL,'" + title + "', date_format(now(),'%Y-%m-%d') ,'" + content + "','" + author + "','" + file_name + "');"
        dbc.execute(sql)




    @classmethod
    def deleteBoard(cls, board_code) -> 'BoardDAO':
        sql = 'delete from board where b_num = ' + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def updateBoard (cls, board_code, title, content) -> 'BoardDAO':
        sql = "update board set b_title = '" + title + "', b_content = '" + content + "' where b_num = " + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def selectBoardSearchCount(cls, keyword, option) -> 'BoardDAO':
        sql = "select count(*) from board where " + option + " like '%" + keyword + "%';"
        return dbc.select(sql)

    @classmethod
    def selectBoardSearchPage(cls, page, limit, keyword, option) -> 'BoardDAO':
        sql = "select * from board where " + option + " like '%" + keyword + "%' order by b_num desc LIMIT " + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)