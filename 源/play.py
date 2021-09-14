# -*- coding: utf-8 -*-
import os
import sys

from ui_1 import Ui_MainWindow
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import win32gui



def pretreatmentHandle():
    hwnd = win32gui.FindWindow("Progman", "Program Manager")
    win32gui.SendMessageTimeout(hwnd, 0x052C, 0, None, 0, 0x03E8)
    hwnd_WorkW = None
    while 1:
        hwnd_WorkW = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        print('hwmd_workw: ', hwnd_WorkW)
        if not hwnd_WorkW:
            continue
        hView = win32gui.FindWindowEx(hwnd_WorkW, None, "SHELLDLL_DefView", None)
        print('hwmd_hView: ', hView)
        if not hView:
            continue
        h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        print('h_1: ',h)
        while h:
            win32gui.SendMessage(h, 0x0010, 0, 0)  # WM_CLOSE
            h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
            print(h)
        break
    return hwnd


h = win32gui.FindWindow(("Progman"), ("Program Manager"))


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.player = QMediaPlayer()
        self.player.setNotifyInterval(10000)
        self.player.setVideoOutput(self.ui.videowidget)
        self.player.setMuted(bool(1 - self.player.isMuted()))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.go()

    def go(self):
        self.ui.videowidget.setFullScreen(True)

        with open("./filename.txt", 'r', encoding='utf-8') as f:
            file_name = f.read()
            if file_name =='':
                file_name = 'lkf.mp4'
        print (file_name)
        if not os.path.exists(file_name):
            sys.exit()


        media = QMediaContent(QUrl(file_name))
        self.player.setMedia(media)

        self.mplayList = QMediaPlaylist()
        self.mplayList.addMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        self.player.setPlaylist(self.mplayList)
        self.mplayList.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

        win_hwnd = int(self.winId())
        video_h = int(self.ui.videowidget.winId())
        win32gui.SetParent(win_hwnd, h)
        win32gui.SetParent(video_h, h)
        win32gui.SetParent(video_h, win_hwnd)

        self.player.play()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pretreatmentHandle()
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


