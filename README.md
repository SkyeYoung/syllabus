# JUST 课表导出

![author-Skye](https://img.shields.io/badge/author-Skye-8F77B5.svg)![license-MIT](https://img.shields.io/github/license/JUST-NC/syllabus)

> 初学 Python 时的练手产物。

## 介绍
本程序用于将江苏科技大学教务系统中的课程表导出为 `ics` 格式的文件。

目前有两种使用方式，一是仅下载、使用 `syllabus.py` 文件，二是下载整个仓库，运行 `web.py` 脚本。

## 食用指南

### 仅使用 `syllabus.py`

1. 下载、打开 `syllabus.py` 文件。
2. 光标定位到文件底部，填写教务系统账户信息和正式开学日期，保存。
3. 运行 `syllabus.py` 。
4. 如无意外，你将在该脚本所属的同一个文件夹中获得扩展名为 `ics` 的课程表文件。
5. 选择你喜欢的日历应用，将刚刚获得的文件导入。

### 使用 `web.py`

1. 下载整个仓库，运行 `web.py` 。
2. 依次输入教务系统的账号、密码，并选择正式开学的日期。
3. 点击 `EXPORT` 按钮。
4. 如果没有意外，`ics` 文件很快就会被下载到你的电脑中。
5. 选择你喜欢的日历应用，将刚刚获得的文件导入。

## 其它

### Web 版低清截图


<img src="/images/web_screenshot_1.png" alt="首页" height="200">
<img src="/images/web_screenshot_2.png" alt="说明" height="200">


### 为什么写这个程序
我曾经看到一篇[文章](https://hfo4.github.io/2017/12/22/e5-b0-86-e8-af-be-e8-a1-a8-e5-af-bc-e5-85-a5-e6-97-a5-e5-8e-86-ef-bc-8c-e8-ae-a9-e6-97-a5-e5-8e-86-e5-86-8d-e6-ac-a1-e4-bc-9f-e5-a4-a7/)，其作者创造了个类似的程序。可惜，我看的时候那个网页已经不能正常访问了，而且我们的教务系统并不一样。所以乘着开始学 Python ，我自己就尝试着实现一下。

虽说我后来有找到那位作者程序的仓库，但是自己太懒了，完全没有看。再加上是新手，所以代码质量什么的……

### 下一步计划

- [ ] 图形界面版本
- [ ] 写一下注释


