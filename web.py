#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import io
import json

from flask import Flask, render_template, request, send_file

from syllabus import generate_syllabus, StepError, get_cal

data = ''

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/export', methods=['POST'])
def export():
    account = {
        'USERNAME': request.form['username'],
        'PASSWORD': request.form['password']
    }
    start_date = [int(x) for x in request.form['date'].split('-')]

    try:
        global data
        data = generate_syllabus(account, (start_date[1], start_date[2]))
    except StepError as err:
        return json.dumps({
            'code': -1,
            'msg': str(err),
        })
    else:
        return json.dumps({
            'code': 1,
            'msg': "",
        })


@app.route('/file', methods=['POST'])
def file():
    global data
    return send_file(io.BytesIO(get_cal(data[0]).encode('UTF-8')), attachment_filename=f'{data[1]}_syllabus.ics',
                     as_attachment=True)


if __name__ == '__main__':
    app.run()
