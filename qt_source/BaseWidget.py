#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys
from ctypes import windll

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication, QMainWindow, QVBoxLayout

from qt_source.LoadQSS import load_qss

BAR_HEIGHT = 24  # 标题高度
BTN_WIDTH = 24  # 按钮宽度
BTN_HEIGHT = 21  # 按钮高度
LABEL_SIZE = 24  # 标签尺寸
SHADOW_SIZE = 8  # 阴影尺寸


class TitleBar(QWidget):
    """自定义标题栏组件，不直接使用，不含图标和标题"""

    def __init__(self, parent):
        super(TitleBar, self).__init__()

        # 开始位置
        self.__start_pos = None
        # 顶层的窗口
        self.__win = parent
        # 是否被按下
        self.__isPressed = False

        """引入样式"""
        self.setAttribute(Qt.WA_StyledBackground, True)  # 设置这个才能设置 QWidget 的背景色
        self.setStyleSheet(load_qss('./style/titlebar.qss'))

        """三大按钮"""
        # 初始化三大按钮
        self.__min_btn = QPushButton(self)
        self.__max_btn = QPushButton(self)
        self.__close_btn = QPushButton(self)

        # 设置三大按钮尺寸
        self.__min_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.__max_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.__close_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)

        # 设置三大按钮图标
        self.__min_btn.setIcon(QIcon('images/icon/minimize.png'))
        self.__max_btn.setIcon(QIcon('images/icon/maximize.png'))

        # 关闭按钮额外设置
        self.__close_btn.setStyleSheet(
            # 鼠标未悬浮状态下
            'QPushButton{border-image:url(images/icon/close.png);}' +
            # 鼠标悬浮状态下
            'QPushButton:hover{background: #e81123; border-image:url(images/icon/close_white.png);}')

        # 设置三大按钮图标大小
        self.__min_btn.setIconSize(QSize(24, 21))
        self.__max_btn.setIconSize(QSize(24, 21))
        self.__close_btn.setIconSize(QSize(24, 21))

        # 设置三大按钮点击事件
        self.__min_btn.clicked.connect(self.__minimize_window)
        self.__max_btn.clicked.connect(self.__maximize_window)
        self.__close_btn.clicked.connect(self.__close_window)

        """布局"""
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        # 布局样式
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignRight)

        # 添加三大按钮到标题栏
        layout.addWidget(self.__min_btn)
        layout.addWidget(self.__max_btn)
        layout.addWidget(self.__close_btn)

    def __minimize_window(self):
        """最小化窗口"""
        self.__win.showMinimized()

    def __maximize_window(self):
        """最大化窗口"""
        if self.__win.isMaximized():
            self.__win.showNormal()
            # 调整为全屏图标
            self.__max_btn.setIcon(QIcon('images/icon/maximize.png'))
        else:
            self.__win.showMaximized()
            # 调整为重置图标
            self.__max_btn.setIcon(QIcon('images/icon/restore.png'))

    def __close_window(self):
        """关闭窗口"""
        self.__win.close()

    def mouseDoubleClickEvent(self, event):
        """重写，鼠标双击事件"""
        self.__close_window()
        return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        """重写，鼠标单击事件"""
        self.__isPressed = True
        self.__start_pos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """重写，鼠标释放事件"""
        self.__isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """重写，鼠标移动事件"""
        if self.__isPressed:
            if self.__win.isMaximized:
                self.__win.showNormal()

            move_pos = event.globalPos() - self.__start_pos
            self.__start_pos = event.globalPos()
            self.__win.move(self.__win.pos() + move_pos)

        return QWidget().mouseMoveEvent(event)


class RawWindow(QMainWindow):
    """自定义窗体，不直接使用"""

    def __init__(self, body):
        super(RawWindow, self).__init__()

        # 真正用于存放组件的窗体
        self.__body = body

        """引入样式"""
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无框架窗体，方便使用自定义标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗口背景透明，方便设置阴影
        self.setStyleSheet(load_qss('./style/basewindow.qss'))

        """布局设置"""
        layout = QVBoxLayout(self)  # 垂直布局
        q_self = QWidget(self)  # 将本身转化为 QWidget

        self.setCentralWidget(q_self)
        q_self.setLayout(layout)
        layout.addWidget(TitleBar(self))
        layout.addWidget(self.__body)
        layout.setStretch(1, 100)
        layout.setSpacing(0)
        layout.setContentsMargins(SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE)

    def __draw_shadow(self, painter):
        """绘制左上角、左下角、右上角、右下角、上、下、左、右阴影"""
        pixmaps = list()
        pixmaps.append('images/shadow/left_top.png')
        pixmaps.append('images/shadow/left_bottom.png')
        pixmaps.append('images/shadow/right_top.png')
        pixmaps.append('images/shadow/right_bottom.png')
        pixmaps.append('images/shadow/top_mid.png')
        pixmaps.append('images/shadow/bottom_mid.png')
        pixmaps.append('images/shadow/left_mid.png')
        pixmaps.append('images/shadow/right_mid.png')

        # 左上角
        painter.drawPixmap(0, 0, SHADOW_SIZE, SHADOW_SIZE, QPixmap(pixmaps[0]))
        # 右上角
        painter.drawPixmap(self.width() - SHADOW_SIZE, 0, SHADOW_SIZE, SHADOW_SIZE,
                           QPixmap(pixmaps[2]))
        # 左下角
        painter.drawPixmap(0, self.height() - SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE,
                           QPixmap(pixmaps[1]))
        # 右下角
        painter.drawPixmap(self.width() - SHADOW_SIZE, self.height() - SHADOW_SIZE, SHADOW_SIZE,
                           SHADOW_SIZE, QPixmap(pixmaps[3]))
        # 左
        painter.drawPixmap(0, SHADOW_SIZE, SHADOW_SIZE, self.height() - 2 * SHADOW_SIZE,
                           QPixmap(pixmaps[6]).scaled(SHADOW_SIZE, self.height() - 2 * SHADOW_SIZE))
        # 右
        painter.drawPixmap(self.width() - SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE, self.height() - 2 * SHADOW_SIZE,
                           QPixmap(pixmaps[7]).scaled(SHADOW_SIZE, self.height() - 2 * SHADOW_SIZE))
        # 上
        painter.drawPixmap(SHADOW_SIZE, 0, self.width() - 2 * SHADOW_SIZE, SHADOW_SIZE,
                           QPixmap(pixmaps[4]).scaled(self.width() - 2 * SHADOW_SIZE, SHADOW_SIZE))
        # 下
        painter.drawPixmap(SHADOW_SIZE, self.height() - SHADOW_SIZE, self.width() - 2 * SHADOW_SIZE,
                           SHADOW_SIZE, QPixmap(pixmaps[5]).scaled(self.width() - 2 * SHADOW_SIZE, SHADOW_SIZE))

    def paintEvent(self, event):
        """调用 draw_shadow 绘制阴影"""
        painter = QPainter(self)
        # 调用 draw_shadow
        self.__draw_shadow(painter)
        painter.setPen(Qt.NoPen)
        # 窗口本体是白色
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(SHADOW_SIZE, SHADOW_SIZE, self.width() - 2 * SHADOW_SIZE,
                               self.height() - 2 * SHADOW_SIZE))


class BaseWindow(QWidget):
    def __init__(self):
        super(BaseWindow, self).__init__()
        self.__window = RawWindow(self)

    def show(self) -> None:
        """重写，显示真正的窗口"""
        self.__window.show()

    def setWindowTitle(self, a0: str) -> None:
        """重写，设置真正窗口的标题，只会显示在任务栏"""
        self.__window.setWindowTitle(a0)

    def setWindowIcon(self, icon: QtGui.QIcon) -> None:
        """重写，设置真正窗口的图标，只会显示在任务栏"""
        self.__window.setWindowIcon(icon)


if __name__ == '__main__':
    """测试"""
    # 解决 Windows 下任务栏图标不显示的问题
    my_id = u'syllabus_export.1.0'  # arbitrary string
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_id)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./images/icon/logo.png'))
    window = BaseWindow()
    window.setWindowIcon(QIcon('./images/icon/logo.png'))
    window.setWindowTitle('Just A Test')
    window.show()
    sys.exit(app.exec_())
