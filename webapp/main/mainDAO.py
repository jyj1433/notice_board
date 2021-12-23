import db_connection as dbc

dbc = dbc.db_conn()

class MainDAO:

    @classmethod
    def selectBoardList(cls) -> 'MainDAO':
        sql = "select * from board, users, board_dev, board_free"
        return dbc.select(sql)