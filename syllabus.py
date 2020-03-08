#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO Web界面
# TODO 图形界面

__author__ = 'iskye'

"""syllabus
导出江科大课表为 ics 文件。
Let's Make Calendar Great Again!
"""

import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from requests import Session

# 账户信息
account = {
    'USERNAME': '',
    'PASSWORD': ''
}
# 开学日期
startDate = (2, 17)

#################################################
#     不要修改下面的代码，除非你知道你在做什么     #
#################################################

# 基础链接
url = 'http://jwgl.just.edu.cn:8080/jsxsd/'
# 登录链接
loginURL = '{}xk/LoginToXk'.format(url)
# 课表链接
syllabusURL = '{}xskb/xskb_list.do'.format(url)


class ClassInfo:
    """课程信息"""

    # 星期
    __week = ('mo', 'tu', 'we', 'th', 'fr', 'sat', 'su')
    # 上课时间
    __startTime = ([8, 0], [10, 0], [14, 0], [15, 50], [19, 0])

    def __init__(self, *, arr: list, semester, day, time):
        # 课程号
        self.id = arr[0]
        # 课程名
        self.name = arr[1]
        # 教师
        self.teacher = arr[2]
        # 周次
        self.week_range_text = arr[3]
        self.week_range = [int(x) for x in re.split('[,-]', arr[3][:-3])]
        # 上课地点
        self.classroom = arr[4]
        # 周几
        self.week_text = self.__week[day - 1]
        self.week = day
        # 上课开始时间
        self.time = self.__startTime[time]
        # 日期，顺序依次为年、月、日
        self.date = [int(semester[:4]) if semester[-1] == 1 else int(semester[5:9]), startDate[0], startDate[1]]

    def __str__(self):
        return '课程号：{}，课程名：{}，教师：{}，周次：{}，上课地点：{}'.format(self.id, self.name, self.teacher,
                                                          self.week_range_text, self.classroom)


def get_cal(cal: Calendar) -> str:
    """返回格式化的日历"""
    return cal.to_ical().decode().replace('\r\n', '\n')


def get_cal_event(info: ClassInfo, *, start_week=0, end_week=1) -> Event:
    """返回一个 cal event"""

    # 开始日期
    start_time = datetime(year=info.date[0], month=info.date[1], day=info.date[2], hour=info.time[0],
                          minute=info.time[1]) + timedelta(weeks=info.week_range[start_week] - 1, days=info.week - 1)
    # print(info, '第一次上课时间：', start_time)
    # cal event
    event = Event()
    # 一天中的开始时间
    event.add('dtstart', start_time)
    # 一天中的结束时间
    event.add('dtend', start_time + timedelta(minutes=100))
    # 提前通知的时间
    event.add('trigger', start_time - timedelta(minutes=20))
    # 重复的日期，以及在哪一周结束
    event.add('rrule', {'freq': 'weekly', 'interval': '1', 'byday': info.week_text,
                        'until': start_time + timedelta(weeks=info.week_range[end_week] - 1)})
    # 课程名
    event.add('summary', info.name)
    # 其余课程信息
    event.add('description',
              '课程号：{}\n教师：{}\n周次：{}'.format(info.id, info.teacher, info.week_range_text))
    event.add('location', info.classroom)
    return event


if __name__ == '__main__':
    #############################################
    #                   登录                    #
    #############################################
    # 初始化 session
    session = Session()
    # 登录 & 获取 cookie
    session.post(url=loginURL, data=account)

    #############################################
    #            获取学期时间 & 课表             #
    #############################################
    res = session.get(url=syllabusURL)
    html = BeautifulSoup(res.text, features='html.parser')
    # 获取学期时间文字
    term = html.find_all('option', {'selected': 'selected'})[0].get_text()
    # 课表
    tds = html.find(id='kbtable').find_all_next('div', class_='kbcontent')
    # 存储课表信息
    classTable = []
    # 遍历获取课程信息
    counter = 1
    for td in tds:
        # 提取文字
        classInfo = [text for text in td.stripped_strings]
        # 存储同一时间段内的课程
        classList = []
        # 分别获取课程信息
        if len(classInfo) >= 5:
            classList.append(ClassInfo(arr=classInfo[0:5], semester=term, day=counter % 7, time=(counter - 1) // 7))
            if len(classInfo) == 11:
                classList.append(
                    ClassInfo(arr=classInfo[6:11], semester=term, day=counter % 7, time=(counter - 1) // 7))
        # 将同一时间段内的课程加入到课表信息中
        classTable.append(classList)
        counter += 1

    #############################################
    #                 生成日历                   #
    #############################################
    syllabus = Calendar()
    # 版本，用于支持一些新特性，比如换行什么的
    syllabus.add('version', '2.0')
    # 日历开始时间
    syllabus.add('dtstart', datetime.now())
    # 日历名称
    syllabus.add('summary', '{} syllabus'.format(term))
    # 遍历日历事件
    for courses in classTable:
        for course in courses:
            # TODO 如果有更多的范围该怎么办呢？
            week_range_len = len(course.week_range)
            if week_range_len == 1:
                syllabus.add_component(get_cal_event(course, end_week=0))
            else:
                syllabus.add_component(get_cal_event(course))
                if week_range_len == 4:
                    syllabus.add_component(get_cal_event(course, start_week=2, end_week=3))

    #############################################
    #                 写入文件                   #
    #############################################
    with open('./{}_syllabus.ics'.format(term), 'w', encoding='utf8') as f:
        f.write(get_cal(syllabus))
