import db_connection as dbc

dbc = dbc.db_conn()

class MainDAO:

    @classmethod
    def selectBoardList(cls) -> 'MainDAO':
        sql = 'select board_free.bf_num, board_free.bf_title, users.usr_name as nickname from board_free, users where board_free.bf_author = users.usr_id order by bf_num desc LIMIT 0, 5;'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetail(cls, board_code) -> 'MainDAO':
        sql = 'select board_free.*, users.usr_name as nickname from board_free, users where board_free.bf_author = users.usr_id and board_free.bf_num = ' + board_code + ';'
        return dbc.select(sql)