from flask import Blueprint, render_template, request, send_file, redirect
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
    re = dao.selectBoardAll()  # 게시판 최신글

    # 날짜, 시간
    today = datetime.date.today()  # 오늘 날짜 (년월일)
    tomorrow = str(today + datetime.timedelta(days=1))  # 내일 날짜 (년월일)
    tomorrow = ''.join(tomorrow.split('-'))  # '-' 하이푼 제거 후 병합
    day2 = str(today + datetime.timedelta(days=2))  # 내일 날짜 (년월일)
    day2 = ''.join(day2.split('-'))  # '-' 하이푼 제거 후 병합
    today = ''.join(str(today).split('-'))  # '-' 하이푼 제거 후 병합
    time_now = str(datetime.datetime.now()).split(' ')  # 현재 시간 (년월일,시분초)
    time_now_date = ''.join(time_now[0].split('-'))  # '-' 하이푼 제거 후 병합
    time_now_time = time_now[1].split(':')
    time_now_time = time_now_time[0] + '00'  # '00' 고정값

    # 날씨 정보 api (공공데이터포털 api, xml형식, 단기예보)
    My_API_Key = unquote(
        '9W%2FSk5W5sjKjfkfkg4ewDvPSe70aBvEL3fcnJEABYSv%2BXvOFh38DT33b1qsszbu5TQHRBgH%2BGGubuSVN%2FBR6Aw%3D%3D')  # Service KEY
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

    tomorrowList = []  # 내일 예보 (최저기온, 최고기온)
    todayList = []  # 오늘 예보 (최저기온, 최고기온)
    columnList = []  # 임시 저장 리스트
    tmpList = []  # 현재 온도 리스트
    skyList = []  # 하늘 상태 리스트
    rainList = []  # 강수 상태 리스트(임시리스트)

    update_com = dao.selectWeatherUp()  # 업데이트 row 조회
    if update_com[0][1] == today or (update_com[0][1] != today and int(time_now_time) <= 400):
        weather_total = dao.selectWeather()
        rowsLen = len(weather_total)
        for i in range(0, rowsLen):
            columnsLen = len(weather_total[0]) # 주의! - DB에 num컬럼이 추가로 들어가있음 (api 8컬럼, DB 9컬럼)
            for j in range(0, columnsLen):
                eachColumn = weather_total[i][j]
                columnList.append(eachColumn)

            if columnList[4] == time_now_date and columnList[5] == time_now_time:
                if columnList[3] == "TMP":
                    tmpList = columnList
                if columnList[3] == "SKY":
                    skyList = columnList

            # 오늘 최저, 최고 기온 (오늘 최저 기온의 경우 'TMN-최저기온'으로 안넘겨주기에 'TMP-현재기온'이 06시에 예보된 기온을 가져옴, 'TMN-최저기온' 예보시간이 06시임)
            if (columnList[4] == today and columnList[3] == 'TMX1') or (columnList[4] == today and columnList[3] == 'TMP' and columnList[5] == '0600'):
                splited = columnList[6].split('.')
                columnList[6] = splited[0]
                todayList.append(columnList)

            # 내일 최저, 최고 기온
            if (columnList[4] == tomorrow and columnList[3] == 'TMX2') or (columnList[4] == tomorrow and columnList[3] == 'TMN2'):
                splited = columnList[6].split('.')
                columnList[6] = splited[0]
                tomorrowList.append(columnList)

            columnList = []  # 다음 row의 값을 넣기 위해 비워준다
    else:
        try:
            # api 호출 후 응답받은 데이터 DB에 저장
            response = requests.get(xmlUrl + queryParams, timeout=5).text.encode('utf-8')  # API 호출 및 응답 - 5초 타임아웃 걸려있음
            xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
            weather_rows = xmlobj.findAll('item')

            rowsLen = len(weather_rows)
            for i in range(0, rowsLen):
                columns = weather_rows[i].find_all()
                columnsLen = len(columns)

                for j in range(0, columnsLen):
                    eachColumn = columns[j].text
                    columnList.append(eachColumn)

                # 하늘상태 코드 변환 ( 1-맑음, 2-구름많음, 3-흐림 )
                if columnList[2] == "SKY":
                    if columnList[5] == "1":
                        columnList[5] = "맑음"
                    if columnList[5] == "3":
                        columnList[5] = "구름많음"
                    if columnList[5] == "4":
                        columnList[5] = '흐림'
                    skyList.append(columnList)

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
                    rainList.append(columnList)

                # DB정보 최신화
                if (columnList[2] == "TMP" and columnList[3] == today) or (columnList[2] == "TMP" and columnList[3] == tomorrow and int(columnList[4]) < 600):
                    dao.updateWeather(columnList)
                if columnList[2] == "TMX" and columnList[3] == today:
                    columnList[2] = columnList[2] + "1"
                    dao.updateWeather(columnList)
                if (columnList[2] == "TMX" or columnList[2] == "TMN") and columnList[3] == tomorrow:
                    columnList[2] = columnList[2] + "2"
                    dao.updateWeather(columnList)
                if (columnList[2] == "TMX" or columnList[2] == "TMN") and columnList[3] == day2:
                    columnList[2] = columnList[2] + "3"
                    dao.updateWeather(columnList)

                columnList = []  # 다음 row의 값을 넣기 위해 비워준다

            rowsLen = len(skyList)
            # 하늘상태 업데이트 ( 하늘, 강수상태를 통합후 업데이트 )
            for i in range(0, rowsLen):
                if rainList[i][5] != '없음':
                    skyList[i][5] = rainList[i][5]
                    columnsLen = len(skyList[0])

                for j in range(0, columnsLen):
                    eachColumn = skyList[i][j]
                    columnList.append(eachColumn)

                if columnList[3] == today or (columnList[3] == tomorrow and int(columnList[4]) < 600):
                    dao.updateWeather(columnList)

                columnList = []  # 다음 row의 값을 넣기 위해 비워준다
            dao.updateWeatherUp(today)  # 업데이트 여부 업데이트

            weather_total = dao.selectWeather()
            rowsLen = len(weather_total)
            for i in range(0, rowsLen):
                columnsLen = len(weather_total[0])  # 주의! - DB에 num컬럼이 추가로 들어가있음 (api 8컬럼, DB 9컬럼)
                for j in range(0, columnsLen):
                    eachColumn = weather_total[i][j]
                    columnList.append(eachColumn)

                if columnList[4] == time_now_date and columnList[5] == time_now_time:
                    if columnList[3] == "TMP":
                        tmpList = columnList
                    if columnList[3] == "SKY":
                        skyList = columnList

                # 오늘 최저, 최고 기온 (오늘 최저 기온의 경우 'TMN-최저기온'으로 안넘겨주기에 'TMP-현재기온'이 06시에 예보된 기온을 가져옴, 'TMN-최저기온' 예보시간이 06시임)
                if (columnList[4] == today and columnList[3] == 'TMX1') or (
                        columnList[4] == today and columnList[3] == 'TMP' and columnList[5] == '0600'):
                    splited = columnList[6].split('.')
                    columnList[6] = splited[0]
                    todayList.append(columnList)

                # 내일 최저, 최고 기온
                if (columnList[4] == tomorrow and columnList[3] == 'TMX2') or (
                        columnList[4] == tomorrow and columnList[3] == 'TMN2'):
                    splited = columnList[6].split('.')
                    columnList[6] = splited[0]
                    tomorrowList.append(columnList)

                columnList = []  # 다음 row의 값을 넣기 위해 비워준다
        except:
            print("업데이트에 실패하였습니다.")

    return render_template('index.html', title="index", result=re, today=todayList, tomorrow=tomorrowList, sky=skyList, tmp=tmpList)

# 게시글 상세보기
@bp.route("/main_get", methods=['GET'])
def main_get():
    board_code = request.args.get('idx')
    caption = request.args.get('caption')

    if caption == "자유게시판":
        review = review_view.review_pagenation(board_code, 'b02')
        re = dao.selectBoardDetailFree(board_code)
        return render_template('board_free/board_free_result.html', result=re, title="게시판", page=1, reviewpage=review,
                               idx=board_code, kind=".board_free_get")

    elif caption == "개발일지":
        review = review_view.review_pagenation(board_code, 'b03')
        re = dao.selectBoardDetailDev(board_code)
        return render_template('board_dev/board_dev_result.html', result=re, title="게시판", page=1, reviewpage=review,
                               idx=board_code, kind=".board_dev_get")


@bp.route('/filetest', methods=['GET', 'POST'])  # 파일업로드 테스트 페이지
def filetest():
    if request.method == 'POST':
        f = request.files['file']
        f.save('upload/' + f.filename)
        return render_template('index.html', title="index")
    return render_template('fileTest.html', title="파일테스트")


@bp.route('/fileDown', methods=['GET', 'POST'])
def down_file():
    if request.method == 'POST':
        sw = 0
        files = os.listdir("./upload")
        for x in files:
            if (x == request.form['file']):
                sw = 1

        path = "./upload/"
        return send_file(path + request.form['file'],
                         attachment_filename=request.form['file'],
                         as_attachment=True)