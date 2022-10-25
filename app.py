import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    target = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        path = "/uploads/".join([target, filename])
        file.save(path)
    return path + ' <br>Ok!' + '<br>' + '<img src="uploads/' + filename + '" align="middle" />'

@app.route('/')
def home():
    pass


@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)


if __name__ == '__main__':
    app.run(port=5000)
