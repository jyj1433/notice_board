from flask import render_template, request, Blueprint
import requests
from bs4 import BeautifulSoup

bp = Blueprint("playground", __name__, url_prefix='/')

@bp.route('/fortune', methods=['GET', 'POST'])
def fortune():
    data = request.form
    response = requests.post('https://m.unsin.co.kr/unse/free/today/result', data=data, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')  # html.parser를 사용해서 soup에 넣겠다
    seq = soup.select('p[class="word_txt"]')
    return render_template('playground/playground.html', title="index", seq=seq[0].string)

@bp.route('/playground')
def rockcut():
    return render_template('playground/playground.html', title="index")