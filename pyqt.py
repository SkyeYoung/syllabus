#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow


class BaseWindow(QMainWindow):
    def __init__(self):
        super(BaseWindow, self).__init__()
        # self.diy_window_bar()

    def diy_window_bar(self):
        # 隐藏窗口标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置高度
        self.setFixedHeight(25)

    def move_center(self):
        """窗口居中"""

        # 屏幕几何信息
        screen = QDesktopWidget().geometry()
        # 窗口几何信息
        window = self.geometry()
        # 移动窗口
        self.move((screen.width() - window.width()) / 2, (screen.height() - window.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BaseWindow()
    main.setWindowTitle(' ')
    
    main.resize(400, 200)
    main.move_center()
    main.show()
    sys.exit(app.exec_())
