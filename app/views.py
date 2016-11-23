import os
import sys
import threading
import subprocess
from subprocess import check_output
import uuid
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request
from app import app

import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir) 
import RiperPar

background_scripts = {}

def run_script(file, id):

    out = check_output(["python", "RiperPar.py", file])
    print(out)
    background_scripts[id] = [True, out]

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/is_done')
def is_done():
    id = request.args.get('id', None)
    
    if id not in background_scripts:
        abort(404)
    return jsonify(done=background_scripts[id][0])
    
@app.route('/generate')
def generate():
    id = str(uuid.uuid4())
    background_scripts[id] = [False, None]
    threading.Thread(target=lambda: run_script('fibonacciRecursive.riper', id)).start()
    return render_template('processing.html', id=id)

@app.route('/riper', methods=['POST'])
def riper():
    data = request.form['code']
    code = 'python RiperPar.py "#" ' + data
    process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(out)
    return(str(out))