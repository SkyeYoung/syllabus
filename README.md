# JUST 课表导出

![author-Skye](https://img.shields.io/badge/author-Skye-8F77B5.svg)
![license-MIT](https://img.shields.io/github/license/JUST-NC/syllabus)

> 初学 Python 时的练手产物。

## 介绍
本程序用于将江苏科技大学教务系统中的课程表导出为 ical 格式的文件，以便导入各类日历程序。

目前有三种使用方式，一是仅下载、使用 `syllabus.py` 文件，二是下载整个仓库，运行 `web.py` 文件，三是使用桌面版。

## 食用指南

### 仅使用 `syllabus.py`

1. 下载、打开 `syllabus.py` 文件。
2. 光标定位到文件底部，填写教务系统账户信息和正式开学日期，保存。
3. 运行 `syllabus.py` 。
4. 如无意外，你将在该脚本所属的同一个文件夹中找到扩展名为 ics  的课程表文件。
5. 选择你喜欢的日历应用，将刚刚获得的文件导入。

### 使用 `web.py`

1. 下载整个仓库，使用 [requirements.txt](https://github.com/SkyeYoung/syllabus/blob/master/requirements.txt) 安装依赖。
2. 运行 `web.py` 。
3. 依次输入教务系统的账号、密码，并选择正式开学的日期。
4. 点击 `EXPORT` 按钮。
5. 如果没有意外，扩展名为 ics 的文件很快就会被下载到你的电脑中。
6. 选择你喜欢的日历应用，将刚刚获得的文件导入。

### 使用桌面版

#### 方法一、从 [release](https://github.com/SkyeYoung/syllabus/releases) 中下载，运行。

1. 找到下载下来的可执行文件，点击运行。
2. 依次输入教务系统的账号、密码，并选择正式开学的日期。
3. 如无意外，你将在程序所属的同一个文件夹中找到扩展名为 ics  的课程表文件。
4. 选择你喜欢的日历应用，将刚刚获得的文件导入。

#### 方法二、自行编译，运行。

1. 下载整个仓库，使用 [requirements.txt](https://github.com/SkyeYoung/syllabus/blob/master/requirements.txt) 安装依赖。

2. 安装 `PyInstaller`。

3. 以 Windows 为例，在命令行中输入以下命令：

   ```bash
   # 进入仓库所在目录
   $ cd ./syllabus
   
   # 使用 PyInstaller 打包
   $ pyinstaller -F -w pyqt.py \
   > --name SyllabusDesktop \
   > --add-data "./qt_source/static;static" \
   > --icon "./qt_source/static/images/icon/logo.ico"
   ```

   

4. 进入 `dist` 目录，点击运行 `SyllabusDesktop.exe`

5. 依次输入教务系统的账号、密码，并选择正式开学的日期。

6. 如无意外，你将在当前文件夹下找到扩展名为 ics  的课程表文件。

7. 选择你喜欢的日历应用，将刚刚获得的文件导入。

## 其它

### 网页版截图


<img src="/images/web_screenshot_1.png" alt="首页" height="140">

<img src="/images/web_screenshot_2.png" alt="说明" height="140">

### 桌面版截图

<img src="/images/desktop_screenshot_1.png" alt="欢迎" height="140">

<img src="/images/desktop_screenshot_2.png" alt="输入账户" height="140">

### 为什么写这个程序

我曾经看到一篇[文章](https://hfo4.github.io/2017/12/22/e5-b0-86-e8-af-be-e8-a1-a8-e5-af-bc-e5-85-a5-e6-97-a5-e5-8e-86-ef-bc-8c-e8-ae-a9-e6-97-a5-e5-8e-86-e5-86-8d-e6-ac-a1-e4-bc-9f-e5-a4-a7/)，作者编写了个类似的程序。可惜，我看的时候文中提供的网址已经不能正常访问了，而且我们的教务系统并不一样。所以乘着开始学 Python ，我自己就尝试着实现一下。

虽说我后来通过那篇文章找到了那个程序的仓库，但是我太懒了，完全没有看，大部分的东西还是自己手敲的。再加上是新手，所以代码质量什么的……

### 关于桌面版程序

仿造了我很喜欢的 Telegram 。不过由于我技术能力过低，而且也没参考人家的代码，所以肯定是差了很多吧。

一直很想写个桌面端的软件，在大一也对 Qt 和 Electron 着过迷。可是那时候 Qt 的文档看得我晕头转向，再加上很快被其它东西吸引了，就没有继续尝试。这一次虽然用的不是 C++ 和 QML ，也算遂了愿吧。

（好花时间，以后再也不会写了。）

### 下一步计划

- [x] 桌面版
- [ ] 好好写一下注释


