from flask import Blueprint, render_template, request, send_file
import config
import webapp.main.mainDAO as mainDAO
import os
import modules.review.review_view as review_view
import math
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
    today = datetime.date.today()  # 오늘 날짜 (년월일)
    tomorrow = str(today + datetime.timedelta(days=1))  # 내일 날짜 (년월일)
    tomorrow = ''.join(tomorrow.split('-'))  # '-' 하이푼 제거 후 병합
    today = ''.join(str(today).split('-'))  # '-' 하이푼 제거 후 병합
    time_now = str(datetime.datetime.now()).split(' ')  # 현재 시간 (년월일,시분초)
    time_now_date = ''.join(time_now[0].split('-'))  # '-' 하이푼 제거 후 병합
    time_now_time = time_now[1].split(':')
    time_now_time = time_now_time[0] + '00'  # '00' 고정값

    # 날씨 정보 api (공공데이터포털 api, xml형식, 단기예보)
    My_API_Key = unquote('9W%2FSk5W5sjKjfkfkg4ewDvPSe70aBvEL3fcnJEABYSv%2BXvOFh38DT33b1qsszbu5TQHRBgH%2BGGubuSVN%2FBR6Aw%3D%3D')  # Service KEY
    xmlUrl = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'  # Service URL (단기예보)
    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey'): My_API_Key,
            quote_plus('numOfRows'): '809',
            quote_plus('pageNo'): '1',
            quote_plus('base_date'): time_now_date,
            quote_plus('base_time'): '0500',
            quote_plus('nx'): '56',
            quote_plus('ny'): '125',
        }
    )

    hourList1 = []  # 현재 예보
    hourList2 = []  # 1시간 후 예보
    tomorrowList = []  # 내일 예보 (최저기온, 최고기온)
    todayList = []  # 오늘 예보 (최저기온, 최고기온)
    columnList = []  # 임시 저장 리스트

    try:
        response = requests.get(xmlUrl + queryParams, timeout=5).text.encode('utf-8') # API 호출 및 응답 - 5초 타임아웃 걸려있음
        xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
        weather_rows = xmlobj.findAll('item')

        rowsLen = len(weather_rows)
        for i in range(0, rowsLen):
            columns = weather_rows[i].find_all()
            columnsLen = len(columns)

            for j in range(0, columnsLen):
                eachColumn = columns[j].text
                columnList.append(eachColumn)

            if columnList[3] == time_now_date and columnList[4] == time_now_time:

                # 하늘상태 코드 변환 ( 1-맑음, 2-구름많음, 3-흐림 )
                if columnList[2] == "SKY":
                    if columnList[5] == "1":
                        columnList[5] = "맑음"
                    if columnList[5] == "3":
                        columnList[5] = "구름많음"
                    if columnList[5] == "4":
                        columnList[5] = '흐림'

                # 강수형태 코드 변환 ( 0-없음, 1-비, 2-비/눈, 3-눈, 4-소나기 )
                if columnList[2] == "PTY":
                    if columnList[5] == "0":
                        columnList[5] = "없음"
                    if columnList[5] == "1":
                        columnList[5] = "비"
                    if columnList[5] == "2":
                        columnList[5] = "비/눈"
                    if columnList[5] == "3":
                        columnList[5] = "눈"
                    if columnList[5] == "4":
                        columnList[5] = "소나기"

                hourList1.append(columnList)

            # 오늘 최저, 최고 기온 (오늘 최저 기온의 경우 'TMN-최저기온'으로 안넘겨주기에 'TMP-현재기온'이 06시에 예보된 기온을 가져옴, 'TMN-최저기온' 예보시간이 06시임)
            if (columnList[3] == today and columnList[2] == 'TMX') or (columnList[3] == today and columnList[2] == 'TMP' and columnList[4] == '0600'):
                splited = columnList[5].split('.')
                columnList[5] = splited[0]
                todayList.append(columnList)

            # 내일 최저, 최고 기온
            if (columnList[3] == tomorrow and columnList[2] == 'TMX') or (columnList[3] == tomorrow and columnList[2] == 'TMN'):
                splited = columnList[5].split('.')
                columnList[5] = splited[0]
                tomorrowList.append(columnList)

            columnList = []  # 다음 row의 값을 넣기 위해 비워준다


    except:
        print("api 접속불가")

    return render_template('index.html', title="index", result=re, today=todayList, tomorrow=tomorrowList, hour1=hourList1)

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
        f.save('upload/' + f.filename)
        return render_template('index.html', title="index")
    return render_template('fileTest.html', title="파일테스트")

@bp.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
    if request.method == 'POST':
        sw = 0
        files = os.listdir("./upload")
        for x in files:
            if(x==request.form['file']):
                sw = 1

        path = "./upload/"
        return send_file(path + request.form['file'],
               attachment_filename=request.form['file'],
               as_attachment=True)