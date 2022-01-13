import db_connection as dbc
import modules.review.reviewDAO as reviewDAO

dbc = dbc.db_conn()

class MainDAO(reviewDAO.ReviewDAO):

    @classmethod
    def selectBoardAll(cls) -> 'MainDAO':
        sql = '(select b.bd_num as num, b.bd_title as title, b.bd_datetime as dt, k.k_caption ' \
              'from board_dev b, kind_boards k ' \
              'where b.kind=k.k_code order by dt desc limit 0, 5) ' \
              'union' \
              '(select b.bf_num, b.bf_title, b.bf_datetime as dt, k.k_caption ' \
              'from board_free b, kind_boards k ' \
              'where b.kind=k.k_code order by dt desc limit 0, 5) ' \
              'order by dt desc limit 0, 5;'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetailDev(cls, board_code) -> 'MainDAO':
        sql = 'select board_dev.* ' \
              'from board_dev ' \
              'where board_dev.bd_num = ' + board_code + ';'
        return dbc.select(sql)

    @classmethod
    def selectBoardDetailFree(cls, board_code) -> 'MainDAO':
        sql = 'select board_free.* ' \
              'from board_free ' \
              'where board_free.bf_num = ' + board_code + ';'
        return dbc.select(sql)
