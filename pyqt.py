#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys
from ctypes import windll

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qt_source.basewidget import BaseWindow

if __name__ == '__main__':
    # 解决 Windows 下任务栏图标不显示的问题
    my_id = u'JUST SYLLABUS EXPORT.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_id)

    app = QApplication(sys.argv)
    base_window = BaseWindow()
    base_window.setFixedSize(640, 400)
    # 要想使 move_center 起作用，必须设置 resize
    base_window.resize(640, 400)
    base_window.move_center()
    base_window.setWindowIcon(QIcon('./qt_source/images/icon/logo.png'))
    base_window.setWindowTitle('江科大课表导出 Syllabus Export')
    base_window.show()
    sys.exit(app.exec_())
