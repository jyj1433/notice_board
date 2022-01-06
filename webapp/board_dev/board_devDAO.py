import db_connection as dbc

dbc = dbc.db_conn()

class Board_devDAO:

    @classmethod
    def selectBoardList(cls) -> 'Board_devDAO':
        sql = "select * from board_dev"
        return dbc.select(sql)

    @classmethod
    def selectBoardCount(cls) -> 'Board_devDAO':
        sql = "select count(*) from board_dev"
        return dbc.select(sql)

    @classmethod
    def selectBoardPage(cls, page, limit) -> 'Board_devDAO':
        sql = 'select  users.usr_name as nickname ,board_dev.* ' \
              'from board_dev, users ' \
              'where board_dev.bd_author = users.usr_id order by bd_num desc LIMIT ' + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetail(cls, board_code) -> 'Board_devDAO':
        sql = 'select board_dev.*, users.usr_name as nickname ' \
              'from board_dev, users ' \
              'where board_dev.bd_author = users.usr_id and board_dev.bd_num = ' + board_code + ';'
        return dbc.select(sql)

    @classmethod
    def insertBoard(cls, title, content, author) -> 'Board_devDAO':
        sql = "insert into board_dev " \
              "values (NULL,'" + title + "', date_format(now(),'%Y-%m-%d') ,'" + content + "','" + author + "', NULL, now(), 'b03');"
        dbc.execute(sql)

    @classmethod
    def insertBoardfile(cls, title, content, author, file_name) -> 'Board_davDAO':
        sql = "insert into board_dev " \
              "values (NULL,'" + title + "', date_format(now(),'%Y-%m-%d') ,'" + content + "','" + author + "','" + file_name + "', now(), 'b03');"
        dbc.execute(sql)

    @classmethod
    def deleteBoard(cls, board_code) -> 'Board_devDAO':
        sql = 'delete from board_dev where bd_num = ' + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def updateBoard(cls, board_code, title, content) -> 'Board_devDAO':
        sql = "update board_dev " \
              "set bd_title = '" + title + "', bd_content = '" + content + "' where bd_num = " + board_code + ";"
        dbc.execute(sql)

    @classmethod
    def selectBoardSearchCount(cls, keyword, option) -> 'Board_devDAO':
        sql = "select count(*) " \
              "from board_dev " \
              "where " + option + " like '%" + keyword + "%';"
        return dbc.select(sql)

    @classmethod
    def selectBoardSearchPage(cls, page, limit, keyword, option) -> 'Board_devDAO':
        sql = "select users.usr_name as nickname, board_dev.* " \
              "from board_dev, users " \
              "where board_dev.bd_author = users.usr_id and " + option + " like '%" + keyword + "%' order by bd_num desc LIMIT " + str((page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)