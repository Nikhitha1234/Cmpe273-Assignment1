import rocksdb
from flask import request
import uuid
import os
import sys
from flask import Flask, request,Response, redirect, url_for
from werkzeug.utils import secure_filename
import subprocess
from subprocess import call

db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))

app = Flask(__name__)

@app.route('/api/v1/scripts', methods=['POST'])
def post_script():
    key = uuid.uuid4().hex
    key_bytes = key.encode('utf-8')
    file = request.files['data']
    value = file.filename
    value_bytes = value.encode('utf-8')
    if file.filename == '':
	flash('No selected file')
        return redirect(request.url)
    else:
        if(not(os.path.exists("./uploads"))):
            os.mkdir("uploads")
        file.save('./uploads/' + secure_filename(file.filename))
    db.put(key_bytes,value_bytes)
    msg= "{\n"+'"'+"script-id"+'"'+":"+'"'+key_bytes+'"'+"\n}\n"
    resp = Response(msg,status=201,mimetype='application/json')
    return resp

@app.route('/api/v1/scripts/<scriptid>', methods=['GET'])
def get_script(scriptid):
    X = scriptid.encode('utf-8')
    value = db.get(X)
    a = "./uploads/" + value
    cd = ["ls","-l"]
    proc = subprocess.Popen([sys.executable,a],stdout=subprocess.PIPE)
    return proc.stdout.read()

if __name__ == '__main__':
    app.run('0.0.0.0')

