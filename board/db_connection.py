import pymysql
import logging
import sys

class db_conn:

    host = "172.30.1.55"
    port = 3306
    database = "dev_board"
    username = "test"
    password = "1234"

    # DB 연결 함수
    def db_connect(self):

        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                db=self.database,
                use_unicode=True,
                charset="utf8"
            )
            return conn

        except:
            logging.error("장비를 정지합니다.")
            sys.exit(1)

    def cursor(self, conn):
        cur = conn.cursor()

        return cur

    ##############################################
    def select(self, sql):

        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()

        return rows

    ##############################################
    def insert(self, sql):

        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        conn.commit()
        conn.close()

    ##############################################
    def update(self, sql):

        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        conn.commit()
        conn.close()

    ##############################################
    def delete(self, sql):

        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        conn.commit()
        conn.close()
