#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""syllabus
导出 ical 格式的 JUST 课表。
Let's Make Calendar Great Again!

※ 单独使用本脚本时，必须在底部 main 处填入账号和正式开学日期。
※ 理论上，使用强智教务系统的都可以在修改网站链接和上课时间后使用本脚本。
"""

__author__ = 'iskye'

import functools
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Union, List, Tuple

from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from requests import Session, exceptions
from requests.adapters import HTTPAdapter

###############################################################################
#                   不要修改下面的代码，除非你知道你在做什么                  #
###############################################################################

# 基础链接
URL = 'http://jwgl.just.edu.cn:8080/jsxsd'
# 登录链接
LOGIN_URL = f'{URL}/xk/LoginToXk'
# 课表链接
SYLLABUS_URL = f'{URL}/xskb/xskb_list.do'
# 上课开始时间
START_TIME = (8, 0), (10, 0), (14, 0), (15, 50), (19, 0)
# 课程时长（单位：min）
DURATION = 100
# 提前通知时间（单位：min）
ADVANCE_NOTICE = 20


###############################################################################
#                               自定义数据类型                                #
###############################################################################

class CourseInfo:
    """课程信息"""

    # 星期
    __week = 'mo', 'tu', 'we', 'th', 'fr', 'sa', 'su'

    def __init__(self, info_list: list, day: int, time: int):
        """
        :param info_list: 包括课程号、课程名、教师、周次、上课地点
        :param day: 周几
        :param time: 开始时间的序号
        """
        # 课程号、课程名、教师、周次文字、上课地点
        self.id, self.name, self.teacher, self.week_range_text, self.classroom = info_list
        # 周次列表
        self.week_range = [int(x) for x in re.split('[,-]', info_list[3][:-3])]
        # 周几
        self.week_text = self.__week[day - 1]  # 文字
        self.week = day  # 数字
        # 上课开始时间
        self.time = START_TIME[time]

    def __str__(self):
        return f'课程号：{self.id}，课程名：{self.name}，教师：{self.teacher}，' + \
               f'周次：{self.week_range_text}，上课地点：{self.classroom}'


def account(username: str, password: str) -> dict:
    return {
        'USERNAME': username,
        'PASSWORD': password
    }


###############################################################################
#                               工具类以及函数                                #
###############################################################################

class StepError(Exception):
    """简单的自定义步骤异常，用于区分步骤中的自定义错误"""

    def __init__(self, *args):
        self.args = args


def color_font(content: str, color: str) -> str:
    """简单的自定义彩色文字，仅前景色为彩色"""
    color_dict = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34
    }
    return f'\033[{color_dict[color]}m{content}\033[0m'


def current_term(start_date: Union[tuple, list]) -> str:
    """将开学日期转化为学期文字
    :param start_date: (年, 月, 日)
    :return: 学期，类似 2019-2020-2
    """
    if 1 < start_date[1] < 4:
        return f'{start_date[0] - 1}-{start_date[0]}-2'
    elif 8 < start_date[1] < 11:
        return f'{start_date[0]}-{start_date[0] + 1}-1'
    else:
        raise StepError('开学日期格式错误')


def step_status(step: str, success: str = '', failed: str = '', *, is_rewrite: bool = False):
    """简单的装饰器
    :param step: 步骤文字
    :param success: 成功文字，一般不定义
    :param failed: 失败文字，一般不定义
    :param is_rewrite: 为真时，step, success, failed 都需要完全重写
    :return: 执行函数结果
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 是否直接执行本脚本
            is_main = __name__ == '__main__'
            # 直接执行时打印
            is_main and print(step if is_rewrite else f'STEP: {step}', end='\t')
            try:
                result = func(*args, **kwargs)
            except StepError:
                is_main and print(failed if is_rewrite else color_font('失败', 'red'))
                # 继续抛出错误
                raise
            else:
                is_main and print(success if is_rewrite else color_font('成功', 'green'))
                # 返回函数执行结果
                return result

        return wrapper

    return decorator


def format_cal(cal: Calendar) -> str:
    """返回格式化的日历"""
    return cal.to_ical().decode().replace('\r\n', '\n')


def get_cal_event(info: CourseInfo, start_date: Union[tuple, list], *, start_week=0, end_week=1) -> Event:
    """返回一个 cal event
    :param info: 课程信息
    :param start_date: 正式开学的第一天，格式为 (年,月,日)
    :param start_week: 开始星期的序号，0 开始
    :param end_week: 结束星期的序号，0 开始
    :return: Calender Event
    """
    # 初始化 event
    event = Event()
    # 开始日期
    start_time = datetime(year=start_date[0], month=start_date[1], day=start_date[2], hour=info.time[0],
                          minute=info.time[1]) + timedelta(weeks=info.week_range[start_week] - 1, days=info.week - 1)
    # 一天中的开始时间
    event.add('dtstart', start_time)
    # 一天中的结束时间
    event.add('dtend', start_time + timedelta(minutes=DURATION))
    # 提前通知的时间
    event.add('trigger', start_time - timedelta(minutes=ADVANCE_NOTICE))
    # 重复的日期，以及在哪一周结束
    event.add('rrule', {'freq': 'weekly', 'interval': '1', 'byday': info.week_text,
                        'until': start_time + timedelta(
                            weeks=(info.week_range[end_week] - info.week_range[start_week]))})
    # 课程名
    event.add('summary', info.name)
    # 上课地址
    event.add('location', info.classroom)
    # 其余课程信息
    event.add('description',
              f'课程号：{info.id}\n教师：{info.teacher}\n周次：{info.week_range_text}')
    return event


###############################################################################
#                               生成及导出步骤                                #
###############################################################################

# 之所以这么写是因为 Pycharm 不能正确解析 \b
@step_status(f'STEP: 登录系统\t{color_font("连接中...", "blue")}', f'\rSTEP: 登录系统\t{color_font("成功", "green")}',
             f'\rSTEP: 登录系统\t{color_font("失败", "red")}', is_rewrite=True)
def login(session: Session, account_info: Dict[str, str]) -> Session:
    """登录 & 获取 cookie"""
    try:
        res = session.post(url=LOGIN_URL, data=account_info, timeout=10)
    except exceptions.RequestException:
        raise StepError('登录出现意外，请再试一次')
    else:
        login_html = BeautifulSoup(res.text, features='lxml')
        # 查看是否登录成功
        if len(login_html.find_all('font', {'color': 'red'})) > 0:
            raise StepError('用户名、密码错误或不存在')
        else:
            return session


@step_status('获取课表')
def get_syllabus(session: Session, start_date: Union[tuple, list]) -> Tuple[List[List[CourseInfo]], Union[tuple, list]]:
    """获取课表"""
    try:
        res = session.post(url=SYLLABUS_URL, data={'xnxq01id': current_term(start_date), 'sfFD': 1})
    except exceptions.RequestException:
        raise StepError('获取课表出现意外，请再试一次')
    else:
        syllabus_html = BeautifulSoup(res.text, features='lxml')
        tds = syllabus_html.find(id='kbtable').find_all_next('div', class_='kbcontent')
        # 存储课表信息
        class_table = []
        # 遍历获取课程信息
        counter = 1  # 计数器
        for td in tds:
            # 提取文字
            class_info = [text for text in td.stripped_strings]
            # 存储同一时间段内的课程
            class_list = []
            # 分别获取课程信息
            if len(class_info) >= 5:
                # 同一时间段的第一个课
                class_list.append(
                    CourseInfo(class_info[0:5], counter % 7, (counter - 1) // 7)
                )
                if len(class_info) == 11:
                    class_list.append(
                        CourseInfo(class_info[6:11], counter % 7, (counter - 1) // 7)
                    )
            # 将同一时间段内的课程加入到课表信息中
            class_table.append(class_list)
            counter += 1
        return class_table, start_date


@step_status('生成日历')
def build_calender(class_table: List[List[CourseInfo]], start_date: Union[tuple, list]) -> Tuple[Calendar, str]:
    """生成日历
    :param class_table:
    :param start_date: (年,月,日)
    :return:
    """
    calender = Calendar()
    # 版本，用于支持一些新特性，比如换行什么的
    calender.add('version', '2.0')
    # 日历开始时间
    calender.add('dtstart', datetime.now())
    # 日历名称
    calender.add('summary', f'{current_term(start_date)} syllabus')
    # 遍历日历事件
    for courses in class_table:
        for course in courses:
            # TODO 如果有更多的范围该怎么办呢？
            week_range_len = len(course.week_range)
            if week_range_len == 1:  # 只在某一周上课
                calender.add_component(get_cal_event(course, start_date, end_week=0))
            else:
                calender.add_component(get_cal_event(course, start_date))  # 一个周次范围
                if week_range_len == 4:  # 第二个周次范围
                    calender.add_component(get_cal_event(course, start_date, start_week=2, end_week=3))

    return calender, current_term(start_date)


def generate_syllabus(account_info: Dict[str, str], start_date: Union[tuple, list]) -> Tuple[Calendar, str]:
    """生成课表，执行上方三个步骤
    :param account_info: 账户信息
    :param start_date: (年,月,日)
    :return: Calender, str
    """
    # 初始化 session
    session = Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'})
    # 失败后最多再尝试两次（共三次）
    session.mount('http://', HTTPAdapter(max_retries=2))
    session.mount('https://', HTTPAdapter(max_retries=2))

    return build_calender(*get_syllabus(login(session, account_info), start_date))


@step_status('导出文件')
def export_ics(calender: Calendar, term: str) -> None:
    """导出 .ics 文件
    :param calender: Calender
    :param term: 学期文字，类似 2019-2020-2
    """
    with open(f'./{term}_syllabus.ics', 'w', encoding='utf8') as f:
        f.write(format_cal(calender))


if __name__ == '__main__':
    """单文件模式"""

    # 账户信息
    """单独使用本脚本时，需要在此处填入账号和正式开学日期！！！"""
    self_account = account('', '')
    # 正式开学日期
    startDate = (2020, 2, 17)

    # 生成课表并导出
    try:
        export_ics(*generate_syllabus(self_account, startDate))
    except Exception as err:
        # 打印错误
        print('\n' + color_font(f'Error: {err}', 'red'))
        # 记录错误
        logging.exception(err)
        exit(1)
