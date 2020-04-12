#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'

import os


def load_qss(file_road):
    """导入 .qss 文件，不要带“.”之类的符号"""
    with open(abs_path(file_road), encoding='utf-8') as f:
        return str(f.read())


def get_collection_of_children(*args):
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


def abs_path(road: str):
    """绝对路径，用于解决资源路径问题"""
    return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + road
