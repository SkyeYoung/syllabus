#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys
from ctypes import windll

from PyQt5.QtCore import QDate, QSize, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup, QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFormLayout, QStackedLayout, QLabel, QWidget, QLineEdit, QApplication, \
    QGraphicsOpacityEffect

from qt_source.basewidget import *
from qt_source.tools import load_qss, abs_path
from syllabus import *

# 全局变量
WINDOW_WIDTH = 784  # 窗口宽度
WINDOW_HEIGHT = 552  # 窗口高度

self_account = {}  # 账户信息


class Window(BaseWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.last_index = 0

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        # 要想使 move_center 起作用，必须设置 resize
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.move_center()
        self.setWindowIcon(QIcon(abs_path('static/images/icon/logo.png')))
        self.setWindowTitle('江科大课表导出 v1.0')

        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(StepHello(self.stack_layout))
        self.stack_layout.addWidget(StepAccount(self.stack_layout))
        self.stack_layout.addWidget(StepDate(self.stack_layout))
        self.stack_layout.addWidget(StepSuccess(self.stack_layout))
        self.stack_layout.addWidget(StepMistake(self.stack_layout))
        self.stack_layout.setCurrentIndex(self.last_index)
        self.stack_layout.currentChanged.connect(self.interface_changed)

        self.setLayout(self.stack_layout)
        self.show()

    def interface_changed(self):
        if self.last_index < self.stack_layout.currentIndex():
            self.last_index = self.stack_layout.currentIndex()
        elif self.last_index == 4 and self.stack_layout.currentIndex() == 0:
            for i in range(3)[::-1]:
                self.stack_layout.widget(i).step_ani(True)
            self.last_index = 0
        elif self.last_index in [3, 4] and self.stack_layout.currentIndex() == 2:
            self.stack_layout.widget(2).step_ani(True)
            self.last_index = 2
        elif self.last_index == 2 and self.stack_layout.currentIndex() == 1:
            self.stack_layout.widget(1).step_ani(True)
            self.last_index = 1
        elif self.last_index == 1 and self.stack_layout.currentIndex() == 0:
            self.stack_layout.widget(0).step_ani(True)
            self.last_index = 0


class StepHello(QWidget):
    """欢迎页面"""

    def __init__(self, stack_layout: QStackedLayout):
        super(StepHello, self).__init__()
        self.stack_layout = stack_layout

        self.setStyleSheet(load_qss('static/style/step_hello.qss'))

        self.img = QLabel(self)
        self.img.setPixmap(QPixmap(abs_path('static/images/bg.jpg')))
        self.img.adjustSize()
        self.img.setScaledContents(True)  # 保持大小一样

        self.img_width = self.img.width()
        self.img_height = self.img.height()

        self.title = QLabel(self)
        self.title.setText('JUST Syllabus Export')
        self.title.setObjectName('title')
        self.title.adjustSize()
        self.title.move(276, 243)

        self.title_x = self.title.x()
        self.title_y = self.title.y()

        self.content1 = QLabel(self)
        self.content1.setText('欢迎使用 JUST 课程表导出桌面版客户端')
        self.content1.setObjectName('content')
        self.content1.adjustSize()
        self.content1.move(267, 286)

        self.content1_x = self.content1.x()
        self.content1_y = self.content1.y()

        self.content2 = QLabel(self)
        self.content2.setText('点击下方的按钮，快速开始')
        self.content2.setObjectName('content')
        self.content2.adjustSize()
        self.content2.move(308, 310)

        self.content2_x = self.content2.x()
        self.content2_y = self.content2.y()

        self.btn = BaseButton(self)
        self.btn.setText('快速开始')
        self.btn.move(244, 371)
        self.btn.clicked.connect(self.step_action)

    def step_action(self):
        self.step_ani().finished.connect(lambda: self.stack_layout.setCurrentIndex(1))

    def step_ani(self, is_back=False):
        img_ani = QPropertyAnimation(self.img, b'geometry', self)
        img_ani.setStartValue(QRect(0, 0, self.img_width, self.img_height))
        img_ani.setEndValue(QRect(0, -self.img_height * 2, self.img_width * 2, self.img_height * 2))
        img_ani.setDuration(200)
        img_ani.setEasingCurve(QEasingCurve.OutCurve)

        title_ani = QPropertyAnimation(self.title, b'pos', self)
        title_ani.setStartValue(QPoint(self.title_x, self.title_y))
        title_ani.setEndValue(QPoint(244, 78))
        title_ani.setDuration(200)
        title_ani.setEasingCurve(QEasingCurve.OutCurve)

        content1_ani = QPropertyAnimation(self.content1, b'pos', self)
        content1_ani.setStartValue(QPoint(self.content1_x, self.content1_y))
        content1_ani.setEndValue(QPoint(244, 112))
        content1_ani.setDuration(200)
        content1_ani.setEasingCurve(QEasingCurve.OutCurve)

        content2_ani = QPropertyAnimation(self.content2, b'pos', self)
        content2_ani.setStartValue(QPoint(self.content2_x, self.content2_y))
        content2_ani.setEndValue(QPoint(244, 134))
        content2_ani.setDuration(200)
        content2_ani.setEasingCurve(QEasingCurve.OutCurve)

        # 动画队列
        ani_group = QParallelAnimationGroup(self)
        ani_group.addAnimation(img_ani)
        ani_group.addAnimation(title_ani)
        ani_group.addAnimation(content1_ani)
        ani_group.addAnimation(content2_ani)

        if is_back:
            ani_group.setDirection(ani_group.Backward)

        ani_group.start()

        return ani_group


class StepOthers(QWidget):
    """其它界面的父类"""

    def __init__(self, stack_layout: QStackedLayout):
        super(StepOthers, self).__init__()

        self.stack_layout = stack_layout

        # 样式
        self.setStyleSheet(load_qss('static/style/step_others.qss'))

        # 返回按钮
        self.back_btn = BackButton(self, stack_layout=stack_layout)
        self.back_btn.move(20, 19)

        self.title = QLabel(self)
        self.title.setObjectName('title')
        self.title.move(244, 78)

        self.content1 = QLabel(self)
        self.content1.setObjectName('content')
        self.content1.adjustSize()
        self.content1.move(244, 112)

        self.content2 = QLabel(self)
        self.content2.setObjectName('content')
        self.content2.adjustSize()
        self.content2.move(244, 134)

        self.btn = BaseButton(self)
        self.btn.move(244, 371)

    @staticmethod
    def set_text(label: QLabel, text: str):
        label.setText(text)
        label.adjustSize()


class StepOthersWithForm(StepOthers):
    """带有表单的界面的父类"""

    def __init__(self, stack_layout: QStackedLayout):
        super(StepOthersWithForm, self).__init__(stack_layout)

        # 添加表单
        self.form = QWidget(self)
        self.form_layout = QFormLayout()
        self.form.setLayout(self.form_layout)

    def fade_to_left_ani(self, widget: QWidget):
        widget_move_ani = QPropertyAnimation(widget, b'pos', self)
        widget_move_ani.setStartValue(QPoint(244, widget.y()))
        widget_move_ani.setEndValue(QPoint(50, widget.y()))
        widget_move_ani.setDuration(200)
        widget_move_ani.setEasingCurve(QEasingCurve.InCurve)

        opacity = QGraphicsOpacityEffect(self)
        opacity.setOpacity(1.0)
        widget.setGraphicsEffect(opacity)

        widget_fade_ani = QPropertyAnimation(opacity, b'opacity', self)
        widget_fade_ani.setStartValue(1.0)
        widget_fade_ani.setEndValue(0.0)
        widget_fade_ani.setDuration(200)
        widget_fade_ani.setEasingCurve(QEasingCurve.InCurve)

        return widget_move_ani, widget_fade_ani

    def step_action(self, **kwargs):
        pass

    def step_ani(self, is_back=False):
        title_move_ani, title_fade_ani = self.fade_to_left_ani(self.title)
        content1_move_ani, content1_fade_ani = self.fade_to_left_ani(self.content1)
        content2_move_ani, content2_fade_ani = self.fade_to_left_ani(self.content2)
        form_move_ani, form_fade_ani = self.fade_to_left_ani(self.form)

        # 动画队列
        ani_group = QParallelAnimationGroup(self)
        ani_group.addAnimation(title_move_ani)
        ani_group.addAnimation(title_fade_ani)
        ani_group.addAnimation(content1_move_ani)
        ani_group.addAnimation(content1_fade_ani)
        ani_group.addAnimation(content2_move_ani)
        ani_group.addAnimation(content2_fade_ani)
        ani_group.addAnimation(form_move_ani)
        ani_group.addAnimation(form_fade_ani)

        if is_back:
            ani_group.setDirection(ani_group.Backward)

        ani_group.start()

        return ani_group


class StepAccount(StepOthersWithForm):
    """账户信息页"""

    def __init__(self, stack_layout: QStackedLayout):
        super(StepAccount, self).__init__(stack_layout)

        # 文字
        self.set_text(self.title, '您的教务系统账户信息')
        self.set_text(self.content1, '请依次输入账号、密码。')
        self.set_text(self.content2, '除了教务网，它们不会被上传到任何地方。')

        # 表单
        self.form_layout.setVerticalSpacing(35)
        username_label = EditLabel('账号')
        password_label = EditLabel('密码')
        username_edit = LineEdit()
        username_edit.setMaxLength(12)
        username_edit.setFixedSize(QSize(244, 30))
        password_edit = LineEdit()
        password_edit.setMaxLength(16)
        password_edit.setFixedSize(QSize(244, 30))
        password_edit.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow(username_label, username_edit)
        self.form_layout.addRow(password_label, password_edit)
        self.form.move(244, 206)

        # 底部按钮
        self.btn.setText('下一步')
        self.btn.clicked.connect(lambda: self.step_action(username_edit.text(), password_edit.text()))

    def step_action(self, username: str, password: str):
        # 更新账户信息
        self_account.update(account(username, password))
        # 切换到第三个界面
        self.step_ani().finished.connect(lambda: self.stack_layout.setCurrentIndex(2))


class StepDate(StepOthersWithForm):
    """填写正式开学日期"""

    def __init__(self, stack_layout):
        super(StepDate, self).__init__(stack_layout)

        # 文字
        self.set_text(self.title, '正式开学日期')
        self.set_text(self.content1, '请选择开学的第一天，')
        self.set_text(self.content2, '所有的课程安排将依此计算。')

        # 表单
        self.form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.form_layout.setVerticalSpacing(16)
        date_label = EditLabel('开学日期')
        date_edit = DateEdit(QDate.currentDate())
        self.form_layout.addRow(date_label, date_edit)
        self.form.adjustSize()
        self.form.move(244, (WINDOW_HEIGHT - self.form.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        # 底部按钮
        self.btn.setText('下一步')
        self.btn.clicked.connect(lambda: self.step_action(date_edit.date()))

    def step_action(self, date: QDate):
        index = 0

        try:
            export_ics(*generate_syllabus(self_account, (date.year(), date.month(), date.day())))
        except StepError as err_msg:
            # 设置 err_msg
            StepMistake.set_err_msg(err_msg)
            # 切换到第五个界面，即失败界面
            index = 4
        else:
            # 切换到第四个界面，即成功界面
            index = 3
        finally:
            self.step_ani().finished.connect(lambda: self.stack_layout.setCurrentIndex(index))


class StepSuccess(StepOthers):
    """成功页"""

    def __init__(self, stack_layout: QStackedLayout):
        super(StepSuccess, self).__init__(stack_layout)

        # 返回按钮
        self.back_btn.clicked.connect(lambda: self.back_btn.set_interface(2))

        # 文字
        self.set_text(self.title, '成功了！')
        self.set_text(self.content1, '学校的服务器居然承受住了本次访问。')
        self.set_text(self.content2, '请尽情享受吧。')

        # 成功信息
        success_msg = QLabel(self)
        success_msg.setText('ヾ(≧▽≦*)o')
        success_msg.setObjectName('suc-msg')
        success_msg.adjustSize()
        success_msg.move((WINDOW_WIDTH - success_msg.width()) / 2,
                         (WINDOW_HEIGHT - success_msg.height() - SHADOW_SIZE - BAR_HEIGHT) / 2)

        # 底部按钮
        self.btn.setText('结束程序')
        self.btn.clicked.connect(self.exit)

    @staticmethod
    def exit():
        window.close()


class StepMistake(StepOthers):
    """错误页"""

    # 需要实例化后调用
    err_msg_label: QLabel

    def __init__(self, stack_layout: QStackedLayout):
        super(StepMistake, self).__init__(stack_layout)

        # 返回按钮
        self.back_btn.clicked.connect(lambda: self.back_btn.set_interface(2))

        # 文字
        self.set_text(self.title, '这下尴尬了...')
        self.set_text(self.content1, '导出过程中出现异常，我们发现了以下错误。')
        self.set_text(self.content2, '请再试一次吧。')

        # 错误信息
        StepMistake.err_msg_label = QLabel(self)

        # 底部按钮
        self.btn.setText('再试一次')
        self.btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(0))

    @classmethod
    def set_err_msg(cls, err_msg: StepError):
        """接收一个 StepError 设置错误标签"""

        StepMistake.err_msg_label.setText(str(err_msg))
        StepMistake.err_msg_label.setObjectName('err-msg')
        StepMistake.err_msg_label.adjustSize()
        StepMistake.err_msg_label.move(
            (WINDOW_WIDTH - StepMistake.err_msg_label.width()) / 2,
            (WINDOW_HEIGHT - StepMistake.err_msg_label.height() - SHADOW_SIZE - BAR_HEIGHT) / 2
        )


if __name__ == '__main__':
    # 解决 Windows 下任务栏图标不显示的问题
    my_id = u'JUST SYLLABUS EXPORT.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_id)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
