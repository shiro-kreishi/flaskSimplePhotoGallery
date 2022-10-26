import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    global filename
    if request.method == 'GET':
        return render_template('upload.html')

    target = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        path = "/uploads/".join([target, filename])
        file.save(path)

    # return path + ' <br>Ok!' + '<br>' + '<img src="uploads/' + filename + '" align="middle" />'
    # return render_template('index.html', uploads=os.listdir('./uploads'))
    return redirect(url_for('home'), code=301, Response=None)


@app.route('/')
def home():
    # return '<h1>Hello</h1>'
    return render_template('index.html', uploads=os.listdir('./uploads'))


@app.route('/image/<filename>')
def image(filename):
    if request.method == 'GET':
        print('View image: ' + filename)
        return render_template('image.html', name=filename)


@app.route('/delete/<path:filename>')
def delete(filename):
    print('delete file: ' + filename)
    os.remove('./uploads/' + filename)
    return redirect(url_for('home'), code=301, Response=None)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    full_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + '/' + filename
    print(full_path)
    # return send_from_directory(full_path, filename)
    return send_file(full_path, as_attachment=True)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)


if __name__ == '__main__':
    app.run(port=5000)
