#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'iskye'


def load_qss(file_road):
    with open(file_road) as f:
        return str(f.read())
