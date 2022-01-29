from flask import Blueprint, render_template, request, send_file, redirect, jsonify
import config
import webapp.common.commonDAO as commonDAO
import os

bp = Blueprint("common", __name__, url_prefix='/')
dao = commonDAO.CommonDAO
config = config.host

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


@bp.route("/addImgSummer", methods=["POST"])
def addImgSummer():
    #Grabbing file:
    img = request.files["file"]    #<------ THIS LINE RIGHT HERE! Is #literally all I needed lol.
    # Below is me replacing the img "src" with my S3 bucket link attached, with the said filename that was added.
    imgURL = 'http://' + config +':5000/static/image/upload/' + img.filename
    return jsonify(url=imgURL)


@bp.route("/imageDown", methods=["POST"])
def imageDown():
    img = request.files["file"]
    img.save('static/image/upload/'+img.filename)
    imgURL = 'http://' + config + ':5000/static/image/upload/' + img.filename
    return jsonify(url=imgURL)

