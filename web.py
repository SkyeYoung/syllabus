#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import io
import json

from flask import Flask, render_template, request, send_file

from syllabus import generate_syllabus, StepError, format_cal, account

# 临时存储数据
data = []

app = Flask(__name__)
app.debug = False


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/export', methods=['POST'])
def export():
    # 账户信息
    self_account = account(request.form['username'], request.form['password'])
    # 将 2020-2-17 这样的字符串用 - 分割，并使每个元素转化为 int 类型
    start_date = [int(x) for x in request.form['date'].split('-')]

    try:
        global data
        data = generate_syllabus(self_account, start_date)
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
    return send_file(io.BytesIO(format_cal(data[0]).encode('UTF-8')), attachment_filename=f'{data[1]}_syllabus.ics',
                     as_attachment=True)


@app.errorhandler(404)
def error_404(err):
    return render_template('error.html', title='404', content='File not found'), 404


if __name__ == '__main__':
    app.run()
