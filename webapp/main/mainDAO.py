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

    # up row 제외한 데이터 전부 조회
    @classmethod
    def selectWeather(cls) -> 'MainDAO':
        sql = 'select * from weather where w_cate != "UP";'
        return dbc.select(sql)

    # 업데이트 여부 조회
    @classmethod
    def selectWeatherUp(cls) -> 'MainDAO':
        sql = 'select * from weather where w_cate = "UP";'
        return dbc.select(sql)

    # 날씨정보 업데이트 ( 조건 : 시간, 카테고리 )
    @classmethod
    def updateWeather(cls, list) -> 'MainDAO':
        sql = 'update weather ' \
              'set ' \
              'w_precast = "' + list[0] + \
              '", w_pretime = "' + list[1] + \
              '", w_cate = "' + list[2] + \
              '", w_cast = "' + list[3] + \
              '", w_time = "' + list[4] + \
              '", w_value = "' + list[5] + \
              '", w_x = "' + list[6] + \
              '", w_y = "' + list[7] + \
              '" where w_time = "' + list[4] + \
              '" and w_cate = "' + list[2] + '";'
        dbc.execute(sql)

    # 업데이트 유무 최신화
    @classmethod
    def updateWeatherUp(cls, date) -> 'MainDAO':
        sql = 'update weather ' \
              'set w_precast = "' + date + \
              '", w_cast = "' + date + \
              '" where w_cate = "' + str('UP') + '";'
        print(sql)
        dbc.execute(sql)