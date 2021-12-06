# db_connection.py
#
# 작성일 : 2021. 11. 25
# 최종 수정 : 2021. 12. 04
#
# mysql DB연결과 DML을 다루기 위한 클래스 정의
#
###################################
import pymysql
import logging
import sys

class db_conn:

    host = "172.30.1.45"    # WIFI 바뀌면 ip주소 확인하고 변경할 것
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
    # 밑의 3개의 insert, update, delete 함수를 execute 하나로 통합.
    # 어차피 코드 완전히 같음
    def execute(self, sql):

        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        conn.commit()
        conn.close()

    # ##############################################
    # def insert(self, sql):
    #
    #     conn = self.db_connect()
    #     cur = self.cursor(conn)
    #     cur.execute(sql)
    #     conn.commit()
    #     conn.close()
    #
    # ##############################################
    # def update(self, sql):
    #
    #     conn = self.db_connect()
    #     cur = self.cursor(conn)
    #     cur.execute(sql)
    #     conn.commit()
    #     conn.close()
    #
    # ##############################################
    # def delete(self, sql):
    #
    #     conn = self.db_connect()
    #     cur = self.cursor(conn)
    #     cur.execute(sql)
    #     conn.commit()
    #     conn.close()
