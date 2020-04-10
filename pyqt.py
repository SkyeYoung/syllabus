#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys
from ctypes import windll

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QStackedLayout, QWidget

from qt_source.basewidget import BaseWindow, BaseButton, BackButton, SHADOW_SIZE, BAR_HEIGHT
from qt_source.tools import load_qss

WINDOW_WIDTH = 784
WINDOW_HEIGHT = 552


class Window(BaseWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # 要想使 move_center 起作用，必须设置 resize
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.move_center()
        self.setWindowIcon(QIcon('./qt_source/images/icon/logo.png'))
        self.setWindowTitle('江科大课表导出 v1.0')

        self.stack_layout = QStackedLayout()
        self.setLayout(self.stack_layout)
        self.stack_layout.addWidget(self.step_1)
        self.stack_layout.addWidget(self.step_2)
        self.stack_layout.addWidget(self.step_3)
        # self.stack_layout.addWidget(self.step_4)
        self.stack_layout.addWidget(self.step_suc)
        self.stack_layout.addWidget(self.step_err)
        self.stack_layout.setCurrentIndex(0)
        self.show()

    @property
    def step_1(self):
        interface = QWidget()
        interface.setStyleSheet(load_qss('/style/step1.qss'))

        img = QLabel(interface)
        img.setPixmap(QPixmap('./qt_source/images/bg.jpg'))
        img.setFixedSize(WINDOW_WIDTH, 207)

        title = QLabel(interface)
        title.setText('JUST Syllabus Export')
        title.setObjectName('title')
        title.adjustSize()
        title.move(276, 243)

        content1 = QLabel(interface)
        content1.setText('欢迎使用 JUST 课程表导出桌面版客户端')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(267, 286)

        content2 = QLabel(interface)
        content2.setText('点击下方的按钮，快速开始')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(308, 310)

        btn = BaseButton(interface)
        btn.setText('快速开始')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(1))

        return interface

    @property
    def step_2(self):
        interface = QWidget()
        interface.setStyleSheet(load_qss('/style/step2.qss'))

        back_btn = BackButton(interface, stack_layout=self.stack_layout)
        back_btn.move(20, 19)

        title = QLabel(interface)
        title.setText('您的教务系统账户信息')
        title.setObjectName('title')
        title.adjustSize()
        title.move(244, 78)

        content1 = QLabel(interface)
        content1.setText('请依次输入账号、密码。')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(244, 112)

        content2 = QLabel(interface)
        content2.setText('除了教务网，它们不会被上传到任何地方。')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(244, 134)

        btn = BaseButton(interface)
        btn.setText('下一步')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(2))

        return interface

    @property
    def step_3(self):
        interface = QWidget()
        interface.setStyleSheet(load_qss('/style/step2.qss'))

        back_btn = BackButton(interface, stack_layout=self.stack_layout)
        back_btn.move(20, 19)

        title = QLabel(interface)
        title.setText('正式开学日期')
        title.setObjectName('title')
        title.adjustSize()
        title.move(244, 78)

        content1 = QLabel(interface)
        content1.setText('请选择开学的第一天，')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(244, 112)

        content2 = QLabel(interface)
        content2.setText('所有的课程安排将依此计算。')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(244, 134)

        btn = BaseButton(interface)
        btn.setText('下一步')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(3))

        return interface

    @property
    def step_suc(self):
        interface = QWidget()
        interface.setStyleSheet(load_qss('/style/step2.qss'))

        back_btn = BackButton(interface, stack_layout=self.stack_layout)
        back_btn.move(20, 19)

        title = QLabel(interface)
        title.setText('成功了！')
        title.setObjectName('title')
        title.adjustSize()
        title.move(244, 78)

        content1 = QLabel(interface)
        content1.setText('服务器居然承受住了本次访问。')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(244, 112)

        content2 = QLabel(interface)
        content2.setText('请尽情享受吧。')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(244, 134)

        success_msg = QLabel(interface)
        success_msg.setText('😉')
        success_msg.setObjectName('success-msg')
        success_msg.setFixedSize(60, 60)
        success_msg.move((WINDOW_WIDTH - success_msg.width()) / 2,
                         (WINDOW_HEIGHT - success_msg.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        btn = BaseButton(interface)
        btn.setText('结束程序')
        btn.move(244, 371)
        btn.clicked.connect(self.exit)

        return interface

    @property
    def step_err(self):
        interface = QWidget()
        interface.setStyleSheet(load_qss('/style/step2.qss'))

        back_btn = BackButton(interface, stack_layout=self.stack_layout)
        back_btn.move(20, 19)

        title = QLabel(interface)
        title.setText('这下尴尬了...')
        title.setObjectName('title')
        title.adjustSize()
        title.move(244, 78)

        content1 = QLabel(interface)
        content1.setText('导出过程中出现异常，我们发现了以下错误。')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(244, 112)

        content2 = QLabel(interface)
        content2.setText('请再试一次吧。')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(244, 134)

        err_msg = QLabel(interface)
        err_msg.setText('账号、密码错误或不存在。')
        err_msg.setObjectName('err-msg')
        err_msg.adjustSize()
        err_msg.move((WINDOW_WIDTH - err_msg.width()) / 2,
                     (WINDOW_HEIGHT - err_msg.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        btn = BaseButton(interface)
        btn.setText('再试一次')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(0))

        return interface

    def exit(self):
        self.close()


if __name__ == '__main__':
    # 解决 Windows 下任务栏图标不显示的问题
    my_id = u'JUST SYLLABUS EXPORT.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_id)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
