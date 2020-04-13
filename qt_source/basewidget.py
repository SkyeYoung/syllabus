#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'
__all__ = ['BaseWindow', 'BaseButton', 'BackButton', 'LineEdit', 'DateEdit', 'EditLabel', 'BAR_HEIGHT', 'BTN_WIDTH',
           'BTN_HEIGHT', 'LABEL_SIZE', 'SHADOW_SIZE']

import typing
from ctypes import windll

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication, QMainWindow, QVBoxLayout, QDesktopWidget, \
    QStackedLayout, QLineEdit, QLabel, QDateEdit

from qt_source.tools import *

###############################################################################
#                               BaseWindow 部分                               #
###############################################################################

BAR_HEIGHT = 21  # 标题高度
BTN_WIDTH = 24  # 按钮宽度
BTN_HEIGHT = 21  # 按钮高度
LABEL_SIZE = 24  # 标签尺寸
SHADOW_SIZE = 6  # 阴影尺寸


class RawTitleBar(QWidget):
    """自定义标题栏组件

    ※ 参考 https://github.com/grayondream/CustomTitleBar
    ※ 不含图标和标题（太丑了）
    ※ 不直接使用
    """

    def __init__(self, parent: QMainWindow, parent_layout: QVBoxLayout):
        """
        :param parent: 顶层窗体
        :param parent_layout: 顶层窗体的布局，用于实现阴影的显隐
        """
        super(RawTitleBar, self).__init__()

        # 开始位置
        self.__start_pos = None
        # 是否被按下
        self.__isPressed = False
        # 顶层的窗体
        self.__win = parent
        # 顶层的布局
        self.__win_layout = parent_layout

        """设置样式"""
        self.setAttribute(Qt.WA_StyledBackground, True)  # 设置这个才能设置 QWidget 的背景色
        self.setStyleSheet(load_qss('static/style/raw_title_bar.qss'))

        """三大按钮"""
        # 初始化三大按钮
        self.__min_btn = QPushButton(self)
        self.__max_btn = QPushButton(self)
        self.__close_btn = QPushButton(self)

        # 设置三大按钮尺寸
        self.__min_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.__max_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
        self.__close_btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)

        # 设置两大按钮图标
        self.__min_btn.setIcon(QIcon(abs_path('static/images/icon/minimize.png')))
        self.__max_btn.setIcon(QIcon(abs_path('static/images/icon/maximize.png')))

        # 关闭按钮额外设置
        self.__close_btn.setStyleSheet(
            'QPushButton{border-image:url(' + abs_path('static/images/icon/close.png') + ');}' +  # 按钮正常状态
            'QPushButton:hover{background: #e81123;' +
            'border-image:url(' + abs_path('static/images/icon/close-hover.png') + ');}' +  # 鼠标悬浮状态
            'QPushButton:disabled{' +
            f'border-image:url(' + abs_path('static/images/icon/close-disable.png') + ');}')  # 按钮禁用状态

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

    def __minimize_window(self) -> None:
        """最小化窗口"""
        self.__win.showMinimized()

    def __maximize_window(self) -> None:
        """最大化窗口"""
        if self.__win.isMaximized():
            self.__win.showNormal()
            # 调整为全屏图标
            self.__max_btn.setIcon(QIcon(abs_path('static/images/icon/maximize.png')))
            self.__win_layout.setContentsMargins(SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE)
        else:
            self.__win.showMaximized()
            # 调整为重置图标
            self.__max_btn.setIcon(QIcon(abs_path('static/images/icon/restore.png')))
            self.__win_layout.setContentsMargins(0, 0, 0, 0)

    def __close_window(self) -> None:
        """关闭窗口"""
        self.__win.close()

    def enable_btn(self, btn_name: str, is_enable: bool):
        if btn_name == 'max_btn':
            self.__max_btn.setEnabled(is_enable)
        elif btn_name == 'min_btn':
            self.__min_btn.setEnabled(is_enable)
        elif btn_name == 'close_btn':
            self.__close_btn.setEnabled(is_enable)
        else:
            raise Exception('按钮名称错误')

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        """重写，鼠标双击事件"""
        self.__close_window()
        return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """重写，鼠标单击事件"""
        self.__isPressed = True
        self.__start_pos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """重写，鼠标释放事件"""
        self.__isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """重写，鼠标移动事件"""
        if self.__isPressed:
            if self.__win.isMaximized:
                self.__win.showNormal()

            move_pos = event.globalPos() - self.__start_pos
            self.__start_pos = event.globalPos()
            self.__win.move(self.__win.pos() + move_pos)

        return QWidget().mouseMoveEvent(event)


class RawWindow(QMainWindow):
    """自定义窗体
    不存放组件，主要用于实现窗体阴影。

    ※ 不直接使用
    """

    def __init__(self, body: QWidget):
        super(RawWindow, self).__init__()

        # 垂直布局
        layout = QVBoxLayout()
        # 将本身转化为 QWidget
        q_self = QWidget(self)
        # 标题栏
        self.__title_bar = RawTitleBar(self, layout)
        # 真正用于存放组件的窗体
        self.__body = body

        """设置样式"""
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无框架窗体，方便使用自定义标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗口背景透明，方便设置阴影

        """布局设置"""
        self.setCentralWidget(q_self)
        q_self.setLayout(layout)
        layout.addWidget(self.__title_bar)
        layout.addWidget(self.__body)
        layout.setStretch(1, 100)
        layout.setSpacing(0)
        layout.setContentsMargins(SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE, SHADOW_SIZE)

    def __draw_shadow(self, painter: QPainter) -> None:
        """绘制左上角、左下角、右上角、右下角、上、下、左、右阴影

        ※ 参考 https://www.jianshu.com/p/add4d4778bd3
        """
        pixmaps = list()
        pixmaps.append(abs_path('static/images/shadow/left_top.png'))
        pixmaps.append(abs_path('static/images/shadow/left_bottom.png'))
        pixmaps.append(abs_path('static/images/shadow/right_top.png'))
        pixmaps.append(abs_path('static/images/shadow/right_bottom.png'))
        pixmaps.append(abs_path('static/images/shadow/top_mid.png'))
        pixmaps.append(abs_path('static/images/shadow/bottom_mid.png'))
        pixmaps.append(abs_path('static/images/shadow/left_mid.png'))
        pixmaps.append(abs_path('static/images/shadow/right_mid.png'))

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

    def set_window_flags(self, type_: typing.Union[Qt.WindowFlags, Qt.WindowType]) -> None:
        """模拟 setWindowFlags """

        # 直接调用无效
        if type_ is None:
            return

        flags = (Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint, Qt.WindowCloseButtonHint)
        # flags 的所有子集
        flags_collection = get_collection_of_children(*flags)

        for flag_col in flags_collection:
            if type_ == get_bit_or_all(flag_col):
                # 先关闭
                self.__title_bar.enable_btn('min_btn', False)
                self.__title_bar.enable_btn('max_btn', False)
                self.__title_bar.enable_btn('close_btn', False)
                # 后显示
                if flags[0] in flag_col:
                    self.__title_bar.enable_btn('min_btn', True)
                if flags[1] in flag_col:
                    self.__title_bar.enable_btn('max_btn', True)
                if flags[2] in flag_col:
                    self.__title_bar.enable_btn('close_btn', True)
                # 既然找到了就可以不再继续了
                break

    def move_center(self) -> None:
        """窗口居中"""
        # 屏幕几何信息
        screen = QDesktopWidget().geometry()
        # 窗口几何信息
        window = self.geometry()
        # 移动窗口
        self.move((screen.width() - window.width()) / 2, (screen.height() - window.height()) / 2)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """重写，调用 draw_shadow 绘制阴影"""
        painter = QPainter(self)
        self.__draw_shadow(painter)


class BaseWindow(QWidget):
    """基础窗体
    样式参考了 Telegram 的桌面版。
    """

    def __init__(self):
        super(BaseWindow, self).__init__()

        self.__window = RawWindow(self)

        """设置样式"""
        self.setAttribute(Qt.WA_StyledBackground, True)  # 设置这个才能设置 QWidget 的背景色
        super().setStyleSheet(load_qss('static/style/base_window.qss'))

    def move_center(self) -> None:
        """窗口居中"""
        self.__window.move_center()

    def setStyleSheet(self, style_sheet: str) -> None:
        """默认带有白色背景"""
        super().setStyleSheet(load_qss('static/style/base_window.qss') + style_sheet)

    def resize(self, *args) -> None:
        if len(args) == 2:
            width, height = args
            self.__window.resize(width + 2 * SHADOW_SIZE, height + 2 * SHADOW_SIZE)
        elif len(args) == 1:
            self.__window.resize(args[0].height() + 2 * SHADOW_SIZE, args[0].width() + 2 * SHADOW_SIZE)

    def setFixedSize(self, *args) -> None:
        if len(args) == 2:
            width, height = args
            self.__window.setFixedSize(width + 2 * SHADOW_SIZE, height + 2 * SHADOW_SIZE)
        elif len(args) == 1:
            self.__window.setFixedSize(args[0].height() + 2 * SHADOW_SIZE, args[0].width() + 2 * SHADOW_SIZE)

        # 因为要阻止全屏，所以要设置下面这句，不然会造成一些错误
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def show(self) -> None:
        """重写，显示真正的窗口"""
        self.__window.show()

    def setWindowTitle(self, title: str) -> None:
        """重写，设置真正窗口的标题，只会显示在任务栏"""
        self.__window.setWindowTitle(title)

    def setWindowIcon(self, icon: QtGui.QIcon) -> None:
        """重写，设置真正窗口的图标，只会显示在任务栏"""
        self.__window.setWindowIcon(icon)

    def setWindowFlags(self, type_: typing.Union[Qt.WindowFlags, Qt.WindowType]) -> None:
        self.__window.set_window_flags(type_)

    def close(self) -> bool:
        return self.__window.close()


###############################################################################
#                               BaseButton 部分                               #
###############################################################################

class BaseButton(QPushButton):
    def __init__(self, *args):
        super(BaseButton, self).__init__(*args)
        self.setStyleSheet(load_qss('static/style/base_button.qss'))
        self.setFixedSize(297, 57)
        self.setCursor(Qt.PointingHandCursor)


###############################################################################
#                               BackButton 部分                               #
###############################################################################

class BackButton(QPushButton):
    def __init__(self, *args, stack_layout):
        super(BackButton, self).__init__(*args)
        self.stack_layout: QStackedLayout = stack_layout

        """设置样式"""
        size = 26
        icon = QPixmap(abs_path('static/images/icon/left_arrow.png')). \
            scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(icon))
        self.setStyleSheet(load_qss('static/style/back_button.qss'))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)

        """设置点击事件"""
        self.clicked.connect(self.set_interface)

    def set_interface(self, index=-1):
        if index <= 0:
            prev = self.stack_layout.currentIndex() - 1
            self.stack_layout.setCurrentIndex(prev if prev >= 0 else 0)
        else:
            self.stack_layout.setCurrentIndex(index)


###############################################################################
#                   LineEdit、DateEdit、EditLabel 部分                         #
###############################################################################

class LineEdit(QLineEdit):
    def __init__(self, *args):
        super(LineEdit, self).__init__(*args)
        self.setStyleSheet(load_qss('static/style/label_edit.qss'))


class DateEdit(QDateEdit):
    def __init__(self, *args):
        super(DateEdit, self).__init__(*args)

        self.setStyleSheet(load_qss('static/style/label_edit.qss') +
                           'DateEdit::down-arrow {border-image:url(' +
                           abs_path('static/images/icon/down.png') + ');}' +
                           'QToolButton#qt_calendar_prevmonth{ qproperty-icon: url(' +
                           abs_path('static/images/icon/left.png') + '); }' +
                           'QToolButton#qt_calendar_nextmonth{ qproperty-icon: url(' +
                           abs_path('static/images/icon/right.png') + '); }'
                           )
        self.setFixedWidth(280)
        self.setCursor(Qt.PointingHandCursor)
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy 年 M 月 d 日')


class EditLabel(QLabel):
    def __init__(self, *args):
        super(EditLabel, self).__init__(*args)
        self.setStyleSheet(load_qss('static/style/label_edit.qss'))


if __name__ == '__main__':
    """演示"""

    # 解决 Windows 下任务栏图标不显示的问题
    my_id = u'test.1.0'  # 随便什么字符串
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_id)

    app = QApplication(sys.argv)
    base_window = BaseWindow()
    # 要想使 move_center 起作用，必须设置 resize
    base_window.resize(640, 400)
    base_window.move_center()
    # 注释掉的是固定大小窗口的演示。
    # base_window.setFixedSize(640, 400)
    base_window.setWindowIcon(QIcon('static/images/icon/logo.png'))
    base_window.setWindowTitle('Just A Test')

    vBoxLayout = QVBoxLayout()
    btn = BaseButton('&q')
    btn.setText('TEST')
    vBoxLayout.addWidget(btn)

    base_window.setLayout(vBoxLayout)
    base_window.show()
    sys.exit(app.exec_())
