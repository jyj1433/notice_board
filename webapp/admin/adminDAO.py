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
              "where usr_name like '%" + keyword + "%' LIMIT " + str((page - 1) * limit) + ',' + str(limit) + ';'
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
        sql = "delete from users where usr_id in ('" + id_list_string + "');"

        return dbc.execute(sql)

    @classmethod
    def selectBoardDumpedAdmin(cls, page, limit) -> 'AdminDAO':
        sql = "select b.bd_num as num, b.bd_title as title, b.bd_nickname as nickname, b.bd_date as dt, k.k_caption as caption, k_code as k " \
              "from board_dev b, kind_boards k " \
              "where b.kind=k.k_code and bd_author is null " \
              "union " \
              "select b.bf_num as num, b.bf_title as title, b.bf_nickname as nickname, b.bf_date as dt, k.k_caption as caption, k_code as k " \
              "from board_free b, kind_boards k " \
              "where b.kind=k.k_code and bf_author is null " \
              "LIMIT " + str((page - 1) * limit) + "," + str(limit) + ";"

        return dbc.select(sql)

    @classmethod
    def selectCountBoardDumpedAdmin(cls) -> 'AdminDAO':
        sql = "select sum(cnt) as count " \
              "from(" \
              "select count(*) as cnt from board_dev b, kind_boards k " \
              "where b.kind=k.k_code and bd_author is null " \
              "union " \
              "select count(*) as cnt from board_free b, kind_boards k " \
              "where b.kind=k.k_code and bf_author is null) " \
              "as cnt;"

        return dbc.select(sql)

    @classmethod
    def deleteBoardDumpedAdmin(cls, list) -> 'AdminDAO':
        num_list_string = "', '".join(list)
        sql = "delete from board where b_num in ('" + num_list_string + "');"

        return dbc.execute(sql)

    @classmethod
    def deleteBoard_freeDumpedAdmin(cls, list) -> 'AdminDAO':
        num_list_string = "', '".join(list)
        sql = "delete from board_free where bf_num in ('" + num_list_string + "');"

        return dbc.execute(sql)

    @classmethod
    def deleteBoard_devDumpedAdmin(cls, list) -> 'AdminDAO':
        num_list_string = "', '".join(list)
        sql = "delete from board_dev where bd_num in ('" + num_list_string + "');"

        return dbc.execute(sql)
