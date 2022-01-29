import db_connection as dbc

dbc = dbc.db_conn()

class CommonDAO:

    @classmethod
    def selectNickname(cls, id) -> 'CommonDAO':

        sql = "select usr_name from users where usr_id = '" + id + "';"

        re = dbc.select(sql)

        return re[0][0]