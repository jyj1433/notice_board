import db_connection as dbc

dbc = dbc.db_conn()

class Board_devDAO:

    @classmethod
    def selectBoardList(cls) -> 'Board_devDAO':
        sql = "select * from board_dev"
        return dbc.select(sql)