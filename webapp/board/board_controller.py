import db_connection as dbc
dbc = dbc.db_conn()

def board_get(board_code):
    sql = 'select * from board where b_num = ' + board_code + ";"
    re = dbc.select(sql)
    return re

def board_write_post(title,content,author):
    error = None
    error_content = None
    if title == '':
        error = "제목을 입력해주세요"
    elif content == '':
        error_content = "내용을 입력해주세요"
    else:
        sql = 'insert into board values (NULL,"' + title + '", date_format(now(),"%Y-%m-%d") ,"' + content + '","' + author + '");'
        dbc.execute(sql)
        return True
    return error,error_content