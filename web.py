#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
