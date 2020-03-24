#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import sys

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication, QMainWindow, QVBoxLayout

from qt_source.loadqss import load_qss

BAR_HEIGHT = 24  # 标题高度
BTN_WIDTH = 24  # 按钮宽度
BTN_HEIGHT = 21  # 按钮高度
LABEL_SIZE = 24  # 标签尺寸
SHADOW_WIDTH = 10


class TitleBar(QWidget):
    """自定义标题栏组件，不含图标和标题"""

    def __init__(self, parent):
        super(TitleBar, self).__init__()

        # 开始位置
        self.start_pos = None
        # 顶层的窗口
        self.win = parent
        # 是否被按下
        self.isPressed = False

        """引入样式"""
        self.setAttribute(Qt.WA_StyledBackground, True)  # 设置这个才能设置 QWidget 的背景色
        self.setStyleSheet(load_qss('./style/titlebar.qss'))

        """三大按钮"""
        # 初始化三大按钮
        self.min_btn = QPushButton(self)
        self.max_btn = QPushButton(self)
        self.close_btn = QPushButton(self)

        # 设置三大按钮尺寸
        self.min_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.max_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.close_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)

        # 设置三大按钮图标
        self.min_btn.setIcon(QIcon('images/icon/minimize.png'))
        self.max_btn.setIcon(QIcon('images/icon/maximize.png'))

        # 关闭按钮额外设置
        self.close_btn.setStyleSheet(
            # 鼠标未悬浮状态下
            'QPushButton{border-image:url(images/icon/close.png);}' +
            # 鼠标悬浮状态下
            'QPushButton:hover{background: #e81123; border-image:url(images/icon/close_white.png);}')

        # 设置三大按钮图标大小
        self.min_btn.setIconSize(QSize(24, 21))
        self.max_btn.setIconSize(QSize(24, 21))
        self.close_btn.setIconSize(QSize(24, 21))

        # 设置三大按钮点击事件
        self.min_btn.clicked.connect(self.show_minimized_window)
        self.max_btn.clicked.connect(self.show_maximized_window)
        self.close_btn.clicked.connect(self.close_window)

        """布局"""
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        # 布局样式
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignRight)

        # 添加三大按钮到标题栏
        self.layout.addWidget(self.min_btn)
        self.layout.addWidget(self.max_btn)
        self.layout.addWidget(self.close_btn)

    def show_minimized_window(self):
        self.win.showMinimized()

    def show_maximized_window(self):
        if self.win.isMaximized():
            self.win.showNormal()
            # 调整为全屏图标
            self.max_btn.setIcon(QIcon('images/icon/maximize.png'))
        else:
            self.win.showMaximized()
            # 调整为重置图标
            self.max_btn.setIcon(QIcon('images/icon/restore.png'))

    def close_window(self):
        self.win.close()

    def mouseDoubleClickEvent(self, event):
        self.show_maximized_window()
        return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.isPressed = True
        self.start_pos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            if self.win.isMaximized:
                self.win.showNormal()

            move_pos = event.globalPos() - self.start_pos
            self.start_pos = event.globalPos()
            self.win.move(self.win.pos() + move_pos)

        return QWidget().mouseMoveEvent(event)


class BaseWindow(QMainWindow):
    def __init__(self):
        super(BaseWindow, self).__init__()

        """引入样式"""
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗口背景透明
        self.setStyleSheet(load_qss('./style/basewindow.qss'))

        self.lay = QVBoxLayout(self)
        self.center = QWidget(self)
        self.client = QWidget(self)
        self.InitializeWindow()

    def InitializeWindow(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.InitializeViews()

    def InitializeViews(self):
        self.setCentralWidget(self.center)

        self.center.setLayout(self.lay)

        title_bar = TitleBar(self)
        self.lay.addWidget(title_bar)
        self.lay.addWidget(self.client)
        self.lay.setStretch(1, 100)
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)

    def draw_shadow(self, painter):
        # 绘制左上角、左下角、右上角、右下角、上、下、左、右边框
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
        painter.drawPixmap(0, 0, SHADOW_WIDTH, SHADOW_WIDTH, QPixmap(pixmaps[0]))
        # 右上角
        painter.drawPixmap(self.width() - SHADOW_WIDTH, 0, SHADOW_WIDTH, SHADOW_WIDTH,
                           QPixmap(pixmaps[2]))
        # 左下角
        painter.drawPixmap(0, self.height() - SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH,
                           QPixmap(pixmaps[1]))
        # 右下角
        painter.drawPixmap(self.width() - SHADOW_WIDTH, self.height() - SHADOW_WIDTH, SHADOW_WIDTH,
                           SHADOW_WIDTH, QPixmap(pixmaps[3]))
        # 左
        painter.drawPixmap(0, SHADOW_WIDTH, SHADOW_WIDTH, self.height() - 2 * SHADOW_WIDTH,
                           QPixmap(pixmaps[6]).scaled(SHADOW_WIDTH, self.height() - 2 * SHADOW_WIDTH))
        # 右
        painter.drawPixmap(self.width() - SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH, self.height() - 2 * SHADOW_WIDTH,
                           QPixmap(pixmaps[7]).scaled(SHADOW_WIDTH, self.height() - 2 * SHADOW_WIDTH))
        # 上
        painter.drawPixmap(SHADOW_WIDTH, 0, self.width() - 2 * SHADOW_WIDTH, SHADOW_WIDTH,
                           QPixmap(pixmaps[4]).scaled(self.width() - 2 * SHADOW_WIDTH, SHADOW_WIDTH))
        # 下
        painter.drawPixmap(SHADOW_WIDTH, self.height() - SHADOW_WIDTH, self.width() - 2 * SHADOW_WIDTH,
                           SHADOW_WIDTH, QPixmap(pixmaps[5]).scaled(self.width() - 2 * SHADOW_WIDTH, SHADOW_WIDTH))

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_shadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(SHADOW_WIDTH, SHADOW_WIDTH, self.width() - 2 * SHADOW_WIDTH,
                               self.height() - 2 * SHADOW_WIDTH))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BaseWindow()
    window.show()
    sys.exit(app.exec_())
