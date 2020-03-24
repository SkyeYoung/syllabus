#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow


class BaseWindow(QMainWindow):
    def __init__(self):
        super(BaseWindow, self).__init__()
        # self.diy_window_bar()

    def diy_window_bar(self):
        # 隐藏窗口标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置高度
        self.setFixedHeight(25)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BaseWindow()
    main.setWindowTitle(' ')

    main.resize(400, 200)
    main.show()
    sys.exit(app.exec_())
