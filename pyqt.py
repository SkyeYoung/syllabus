#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys
from ctypes import windll

from PyQt5.QtCore import QSize, QDate
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QStackedLayout, QWidget, QFormLayout, QLineEdit

from qt_source.basewidget import BaseWindow, BaseButton, BackButton, SHADOW_SIZE, BAR_HEIGHT, LineEdit, EditLabel, \
    DateEdit
from qt_source.tools import load_qss
from syllabus import account

# 全局变量
WINDOW_WIDTH = 784  # 窗口宽度
WINDOW_HEIGHT = 552  # 窗口高度
self_account = {}  # 存储账户信息


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

        self.stack_layout.setCurrentIndex(0)
        self.show()

    @property
    def step_1(self):
        """欢迎页面"""
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
        """填写账户信息"""
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

        """表单部分"""
        form = QWidget(interface)
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(35)
        username_label = EditLabel('账号')
        password_label = EditLabel('密码')
        username_edit = LineEdit()
        username_edit.setMaxLength(12)
        username_edit.setFixedSize(QSize(244, 30))
        password_edit = LineEdit()
        password_edit.setMaxLength(16)
        password_edit.setFixedSize(QSize(244, 30))
        password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow(username_label, username_edit)
        form_layout.addRow(password_label, password_edit)
        form.setLayout(form_layout)
        form.move(244, 206)

        btn = BaseButton(interface)
        btn.setText('下一步')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.step_2_action(username_edit.text(), password_edit.text()))

        return interface

    @property
    def step_3(self):
        """填写正式开学日期"""
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

        """表单部分"""
        form = QWidget(interface)
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        form_layout.setVerticalSpacing(16)
        date_label = EditLabel('开学日期')
        date_edit = DateEdit(QDate.currentDate())
        form_layout.addRow(date_label, date_edit)
        form.setLayout(form_layout)
        form.adjustSize()
        form.move(244, (WINDOW_HEIGHT - form.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        btn = BaseButton(interface)
        btn.setText('下一步')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.step_3_action(date_edit.date()))

        return interface

    @property
    def step_suc(self):
        """成功页面"""
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
        content1.setText('学校的服务器居然承受住了本次访问。')
        content1.setObjectName('content')
        content1.adjustSize()
        content1.move(244, 112)

        content2 = QLabel(interface)
        content2.setText('请尽情享受吧。')
        content2.setObjectName('content')
        content2.adjustSize()
        content2.move(244, 134)

        success_msg = QLabel(interface)
        success_msg.setText('ヾ(≧▽≦*)o')
        success_msg.setObjectName('suc-msg')
        success_msg.adjustSize()
        success_msg.move((WINDOW_WIDTH - success_msg.width()) / 2,
                         (WINDOW_HEIGHT - success_msg.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        btn = BaseButton(interface)
        btn.setText('结束程序')
        btn.move(244, 371)
        btn.clicked.connect(self.exit)

        return interface

    def step_err(self, msg):
        """失败页面"""
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
        err_msg.setText(msg)
        err_msg.setObjectName('err-msg')
        err_msg.adjustSize()
        err_msg.move((WINDOW_WIDTH - err_msg.width()) / 2,
                     (WINDOW_HEIGHT - err_msg.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        btn = BaseButton(interface)
        btn.setText('再试一次')
        btn.move(244, 371)
        btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(0))

        return interface

    def step_2_action(self, username: str, password: str):
        global self_account
        self_account = account(username, password)
        # 切换到第三个界面
        self.stack_layout.setCurrentIndex(2)

    def step_3_action(self, date):
        # try:
        #     export_ics(*generate_syllabus(self_account, (date.year(), date.month(), date.day())))
        # except StepError as err_msg:
        #     # 切换到第五个界面，即失败界面
        #     self.stack_layout.addWidget(self.step_err(err_msg))
        #     self.stack_layout.setCurrentIndex(self.stack_layout.currentIndex() + 1)
        # else:
        # 切换到第四个界面，即成功界面
        self.stack_layout.addWidget(self.step_suc)
        self.stack_layout.setCurrentIndex(self.stack_layout.currentIndex() + 1)

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
