import db_connection as dbc

dbc = dbc.db_conn()

def selectNickname(id):
    sql = "select usr_name from users where usr_id = '" + id + "';"

    re = dbc.select(sql)

    return re[0][0]