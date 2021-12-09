import db_connection as dbc

dbc = dbc.db_conn()

class MemberDAO:

    @classmethod
    def selectUserId(cls) -> 'MemberDAO':
        sql = 'select usr_id from users;'
        return dbc.select(sql)

    @classmethod
    def insertMember(cls,memberlist) -> 'MemberDAO':
        sql = "insert into users values %r;" % (tuple(memberlist),)
        return dbc.execute(sql)
