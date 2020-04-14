#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import os
import sys
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon


def abs_path(path: str) -> str:
    """绝对路径，用于解决资源路径问题"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS.replace('\\', '/') + '/' + path
    else:
        return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/' + path


def load_qss(path: str) -> str:
    """导入 .qss 文件，不要带“.”之类的符号"""
    with open(abs_path(path), encoding='utf-8') as f:
        return str(f.read())


def scaled_icon(width: int, height: int, normal_path: str, disabled_path: str = None):
    """缩放图标
    :param width: 宽
    :param height: 高
    :param normal_path: 正常的图标路径
    :param disabled_path: 禁止的图标路径
    :return: QIcon
    """
    icon = QIcon()

    # 正常状态
    icon.addPixmap(QPixmap(abs_path(normal_path)).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                   QIcon.Normal)

    if disabled_path is not None:
        icon.addPixmap(
            QPixmap(abs_path(disabled_path)).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QIcon.Disabled)

    return icon


def get_collection_of_children(*args) -> List:
    """获取一串数字的子集"""
    n = len(args)
    collection = []

    for i in range(2 ** n):
        children = []
        for j in range(n):
            if (i >> j) % 2 == 1:
                children.append(args[j])
        collection.append(children)
    return collection


def get_bit_or_all(items: list):
    """对列表中的所有项进行按位或运算"""
    result = 0
    if len(items) == 0:
        return None
    else:
        for item in items:
            result |= item
        return result
