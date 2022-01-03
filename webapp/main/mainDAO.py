import db_connection as dbc

dbc = dbc.db_conn()

class MainDAO:

    @classmethod
    def selectBoardAll(cls) -> 'MainDAO':
        sql = '(select b.bd_num as num, b.bd_title as title, b.bd_datetime as dt, k.k_caption' \
              ' from board_dev b, kind_boards k where b.kind=k.k_code order by dt desc limit 0, 5)' \
              ' union' \
              ' (select b.bf_num, b.bf_title, b.bf_datetime as dt, k.k_caption' \
              ' from board_free b, kind_boards k where b.kind=k.k_code order by dt desc limit 0, 5)' \
              ' order by dt desc limit 0, 5;'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetailDev(cls, board_code) -> 'MainDAO':
        sql = 'select board_dev.*, users.usr_name as nickname from board_dev, users where board_dev.bd_author = users.usr_id and board_dev.bd_num = ' + board_code + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetailFree(cls, board_code) -> 'MainDAO':
        sql = 'select board_free.*, users.usr_name as nickname from board_free, users where board_free.bf_author = users.usr_id and board_free.bf_num = ' + board_code + ';'
        return dbc.select(sql)
