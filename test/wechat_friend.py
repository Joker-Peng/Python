# -*- coding:utf-8 -*-
import psutil
import pywinauto
from pywinauto.application import Application


'''
psutil 用于获取微信电脑版的进程信息
pywinauto 用于自动化控制微信电脑版
'''
def getWechat():

    #初始化默认进程
    PID = 0
    #我们把进程ID来提供给PyWinAuto ，以便于链接微信电脑版
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid','name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if 'WeChat.exe' == pinfo['name']:
                PID = pinfo['pid']
    #PyWinAuto实例化并启动应用
    app = Application(backend='uia').connect(process= PID)

    #控制微信电脑版，把朋友圈打开

    win = app['微信']
    pyq_but = win.child_window(title = '朋友圈',control_type = "Button")
    pyq_but.draw_outline()
    cords = pyq_but.rectangle()
    #点击朋友圈按钮
    pywinauto.mouse.click(button = 'left',coords = (cords.left + 10,cords.top + 10))
    pyq_win = app['朋友圈']
    pyq_win.draw_outline()
    #获取朋友窗口里面各个控件结构
    print(f'打印朋友圈控件结构：{pyq_win.dump_tree}')

if __name__ == '__main__':
    getWechat()