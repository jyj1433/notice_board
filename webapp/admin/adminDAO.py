import db_connection as dbc

dbc = dbc.db_conn()

class AdminDAO():

    @classmethod
    def selectMemberAdmin(cls, page, limit) -> 'AdminDAO':
        sql = 'select usr_id, usr_name from users where usr_id != "root" LIMIT ' + str((page - 1) * limit) + ',' + str(
            limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectMemberCountAdmin(cls) -> 'AdminDAO':
        sql = 'select count(*) from users where usr_id != "root";'
        return dbc.select(sql)

    @classmethod
    def selectMemberSearchAdmin(cls, page, limit, keyword) -> 'AdminDAO':
        sql = "select usr_id, usr_name " \
              "from users " \
              "where usr_name like '%" + keyword + "%' LIMIT " + str(
            (page - 1) * limit) + ',' + str(limit) + ';'
        return dbc.select(sql)

    @classmethod
    def selectMemberSearchCountAdmin(cls, keyword) -> 'AdminDAO':
        sql = "select count(*) " \
              "from users " \
              "where usr_id != 'root' and usr_name like '%" + keyword + "%';"
        return dbc.select(sql)

    @classmethod
    def deleteMemberAdmin(cls, list) -> 'AdminDAO':
        id_list_string = "', '".join(list)
        sql = "delete from users where usr_id in ('" + id_list_string + "')"

        return dbc.execute(sql)