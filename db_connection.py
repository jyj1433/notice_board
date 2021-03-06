# db_connection.py
#
# 작성일 : 2021. 11. 25
#
# 12. 04 - dml을 excute함수 하나로 통합
# 12. 20 - config.py 추가, host변수 config에서 받아오게 변경
#
# 최종 수정 : 2021. 12. 20
#
# mysql DB연결과 DML을 다루기 위한 클래스 정의
#
###################################
import pymysql
import logging
import sys
import config

class db_conn:

    host = config.host
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
            sys.exit(1)  # 없을경우 DB에 접속하지못한채로 실행되서 error 발생

    # 커서
    def cursor(self, conn):
        cur = conn.cursor()
        return cur

    # 조회
    def select(self, sql):
        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows

    # insert, update, delete 함수를 execute 하나로 통합.
    def execute(self, sql):
        conn = self.db_connect()
        cur = self.cursor(conn)
        cur.execute(sql)
        conn.commit()
        conn.close()