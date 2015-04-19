#!/bin/python
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from subprocess import call
from imageToBW import imageToBW

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'incoming'
app.config['DOWNLOAD_FOLDER'] = 'builds'
app.config['APP_FOLDER'] = 'simple_analog'
app.config['IMAGE_PATH'] = 'simple_analog/resources/images/back.png'
app.config['BUILD_PATH'] = 'simple_analog/build/simple_analog.pbw'

key = 0
def generateKey():
    global key
    key = 1+key
    return 'key' + str(key)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            key = generateKey()
            path = os.path.join(app.config['UPLOAD_FOLDER'], key)
            file.save(path)

            path = imageToBW(path)

            call(['mv', path, app.config['IMAGE_PATH']])

            os.chdir(app.config['APP_FOLDER'])
            call(['/root/pebble-dev/PebbleSDK-3.0-dp8/bin/pebble', 'build'])
            os.chdir('..')

            call(['mv', app.config['BUILD_PATH'], os.path.join(app.config['DOWNLOAD_FOLDER'], key+'.pbw')])

            return redirect(url_for('fetch_file', key=key+'.pbw'))
        return 'INVALID'

    return '''
    <!doctype html>
    <title>Upload face</title>
    <h1>Upload face</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    <p>Wait a minute, then GET /fetch/[key]</p>
    </form>
    '''

@app.route('/fetch/<key>')
def fetch_file(key):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], key)

if __name__ == '__main__':
    app.debug=True
    app.run()
