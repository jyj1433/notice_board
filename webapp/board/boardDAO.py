import db_connection as dbc

dbc = dbc.db_conn()

class BoardDAO:

    @classmethod
    def selectBoardList(cls) -> 'BoardDAO':
        sql = "select * from board order by b_num desc"
        return dbc.select(sql)

    @classmethod
    def selectBoardPage(cls, page, limit) -> 'BoardDAO':
        sql = 'select * from board LIMIT ' + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetail(cls, board_code) -> 'BoardDAO':
        sql = 'select * from board where b_num = ' + board_code + ";"
        return dbc.select(sql)

    @classmethod
    def insertBoard(cls, title, content, author) -> 'BoardDAO':
        sql = 'insert into board values (NULL,"' + title + '", date_format(now(),"%Y-%m-%d") ,"' + content + '","' + author + '");'
        dbc.execute(sql)
