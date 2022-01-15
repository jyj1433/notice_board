from flask import Blueprint, render_template, request, send_file
import config
import webapp.main.mainDAO as mainDAO
import os
import modules.review.review_view as review_view
import requests, bs4
from urllib.parse import urlencode, quote_plus, unquote
from lxml import html
import datetime

bp = Blueprint("main", __name__, url_prefix='/')
dao = mainDAO.MainDAO
config = config.host

# 초기화면
@bp.route('/')
def index():
    re = dao.selectBoardAll()

    # 날짜, 시간
    time_now = str(datetime.datetime.now()).split(' ')
    time_now_date = ''.join(time_now[0].split('-'))  # 오늘 날짜
    time_now_time = time_now[1].split(':')
    time_now_time = time_now_time[0] + '30'  # 매시간 30분에 데이터 올라옴

    # 날씨 정보 xml (공공데이터포털 api, xml)
    xmlUrl = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'  # Service URL
    My_API_Key = unquote('9W%2FSk5W5sjKjfkfkg4ewDvPSe70aBvEL3fcnJEABYSv%2BXvOFh38DT33b1qsszbu5TQHRBgH%2BGGubuSVN%2FBR6Aw%3D%3D')  # Service KEY
    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey'): My_API_Key,
            quote_plus('numOfRows'): '60',
            quote_plus('pageNo'): '1',
            quote_plus('base_date'): time_now_date,
            quote_plus('base_time'): time_now_time,
            quote_plus('nx'): '55',
            quote_plus('ny'): '127',
        }
    )

    response = requests.get(xmlUrl + queryParams).text.encode('utf-8')
    xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
    rows = xmlobj.findAll('item')

    rowList = [] # 전체 리스트
    tempList = []  # 기온 리스트
    rainList = []  # 강수량 리스트
    skyList = []  # 하늘 리스트
    columnList = []  # 임시 저장 리스트
    rowsLen = len(rows)

    for i in range(0, rowsLen):
        columns = rows[i].find_all()
        columnsLen = len(columns)

        for j in range(0, columnsLen):
            eachColumn = columns[j].text
            columnList.append(eachColumn)

        # T1H : 기온(c), RN1 : 1시간 강수량(mm), SKY : 하늘상태
        if columnList[2] == 'T1H':
            tempList.append(columnList)
        elif columnList[2] == 'RN1':
            rainList.append(columnList)
        elif columnList[2] == 'SKY':  # 코드 변환 - 맑음(1), 구름많음(3), 흐림(4)
            if columnList[5] == '1':
                columnList[5] = "맑음"
            elif columnList[5] == '3':
                columnList[5] = "구름많음"
            elif columnList[5] == '4':
                columnList[5] = "흐림"
            skyList.append(columnList)

        rowList.append(columnList)
        columnList = []  # 다음 row의 값을 넣기 위해 비워준다

    return render_template('index.html', title="index", result=re, temp=tempList, rain=rainList, sky=skyList)

# 게시글 상세보기
@bp.route("/main_get", methods=['GET'])
def main_get():
    board_code = request.args.get('idx')
    caption = request.args.get('caption')

    if caption == "자유게시판":
        review = review_view.review_pagenation(board_code,'b02')
        re = dao.selectBoardDetailFree(board_code)
        return render_template('board_free/board_free_result.html', result=re, title="게시판", page=1, reviewpage=review, idx=board_code, kind=".board_free_get")

    elif caption == "개발일지":
        review = review_view.review_pagenation(board_code,'b03')
        re = dao.selectBoardDetailDev(board_code)
        return render_template('board_dev/board_dev_result.html', result=re, title="게시판", page=1,  reviewpage=review, idx=board_code, kind=".board_dev_get")


@bp.route('/filetest',methods=['GET', 'POST']) # 파일업로드 테스트 페이지
def filetest():
    if request.method == 'POST':
        f = request.files['file']
        f.save('upload/'+ f.filename)
        return render_template('index.html', title="index")
    return render_template('fileTest.html', title="파일테스트")

@bp.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
    if request.method == 'POST':
        sw=0
        files = os.listdir("./upload")
        for x in files:
            if(x==request.form['file']):
                sw=1

        path = "./upload/"
        return send_file(path + request.form['file'],
                attachment_filename = request.form['file'],
                as_attachment=True)