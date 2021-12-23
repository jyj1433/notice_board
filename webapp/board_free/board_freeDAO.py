import db_connection as dbc

dbc = dbc.db_conn()

class Board_freeDAO:

    @classmethod
    def selectBoardList(cls) -> 'Board_freeDAO':
        sql = "select * from board_free"
        return dbc.select(sql)