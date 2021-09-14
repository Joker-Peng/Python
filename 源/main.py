# -*- coding: utf-8 -*-



import os
import sys
from subprocess import call
from threading import Thread
from time import sleep

import cv2
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtCore import Qt,  QTimer
from PyQt5.QtGui import QImage, QPixmap, QIcon

from PyQt5.QtWidgets import QGridLayout, QPushButton, QMainWindow, QFileDialog, QLabel, QSystemTrayIcon, \
    QAction, QMenu, QMessageBox
from os import path as pathq


path = ''

def MyMainWindow():
    pass


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.frame = []  # 存图片
        self.detectFlag = False  # 检测flag
        self.cap = []
        self.timer_camera = QTimer()  # 定义定时器
        self.icon_quit()
        try:

            icon_path = pathq.join(pathq.dirname(__file__), './2.ico')

            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))  # 这是对的。
            MainWindow.setWindowIcon(icon)
        except:
            pass


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(505, 615)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(22, 10, 89, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openmp4)
        self.pushButton.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(22, 50, 452, 351))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(11, 20, 430, 291))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QLabel(self)
        self.label.resize(400, 300)
        self.label.setText("Waiting for video...")
        self.gridLayout_3.addWidget(self.label)



        self.close_widget = QtWidgets.QWidget(self.centralwidget)
        self.close_widget.setGeometry(QtCore.QRect(420, 0, 93, 41))

        self.close_widget.setObjectName("close_widget")
        self.close_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.close_widget.setLayout(self.close_layout)  # 设置左侧部件布局为网格

        self.left_close = QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit = QPushButton("")  # 空白按钮
        #self.left_visit.clicked.connect(MainWindow.big)
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(MainWindow.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.close_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(77, 440, 133, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.play)
        self.pushButton_2.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(308, 440, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close_wall)
        self.pushButton_3.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(187, 540, 133, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.openurl)
        self.pushButton_4.setStyleSheet(
            '''QPushButton{background:#222225;color:white;border-radius:5px;}QPushButton:hover{background:#222225;color:skyblue}''')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 505, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.centralwidget.setStyleSheet('''
             QWidget#centralwidget{
             color:white;
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-right:1px solid #222225;
             border-left:1px solid #444444;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-left-radius:10px;
             border-bottom-right-radius:10px;
             }
            
              ''')
        self.groupBox.setStyleSheet('''
        color:white
        ''')

        MainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

    def openurl(self):
        os.system('explorer http://bbs.huoying666.com/forum-53-1.html')

    def icon_quit(self):
        self.mini_icon = QSystemTrayIcon(self)
        self.mini_icon.setIcon(QIcon('./2.ico'))
        quit_menu = QAction('退出软件', self, triggered=self.quitApp)
        quit_menu2 = QAction('关闭壁纸', self, triggered=self.close_wall)
        quit_menu3 = QAction('主界面', self, triggered=MainWindow.show)
        tpMenu = QMenu(self)
        tpMenu.addAction(quit_menu3)
        tpMenu.addAction(quit_menu2)
        tpMenu.addAction(quit_menu)
        self.mini_icon.setContextMenu(tpMenu)
        self.mini_icon.show()




        self.mini_icon.messageClicked.connect(self.message)
        self.mini_icon.activated.connect(self.act)

    def message(self):
        print("弹出的信息被点击了")


    def act(self,reason):
        if reason == 2 or reason == 3:
            MainWindow.show()

    def quitApp(self):
            sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "从本地选择"))
        self.groupBox.setTitle(_translate("MainWindow", "预览"))
        self.pushButton_2.setText(_translate("MainWindow", "应用"))
        self.pushButton_3.setText(_translate("MainWindow", "关闭壁纸"))
        self.pushButton_4.setText(_translate("MainWindow", "在线资源"))

    def openmp4(self):
        try:
            global path
            path, filetype = QFileDialog.getOpenFileName(None, "选择文件", '.',
                                                         "视频文件(*.AVI;*.mov;*.rmvb;*.rm;*.FLV;*.mp4;*.3GP)")  # ;;All Files (*)
            if path == "":  # 未选择文件
                return

            self.slotStart()
            t = Thread(target=self.Stop)
            t.start()  # 启动线程，即让线程开始执行
        except Exception as e:
            print (e)


    def Stop(self):
        """ Slot function to stop the programme
            """
        sleep(30)
        if self.cap != []:
            self.cap.release()
            self.timer_camera.stop()   # 停止计时器

        else:

            Warming = QMessageBox.warning(self, "Warming", "Push the left upper corner button to Quit.",QMessageBox.Yes)

    def slotStart(self):
        """ Slot function to start the progamme
            """
        videoName = path
        if videoName != "":  # “”为用户取消
            self.cap = cv2.VideoCapture(videoName)
            self.timer_camera.start(50)
            self.timer_camera.timeout.connect(self.openFrame)



    def openFrame(self):
        """ Slot function to capture frame and process it
            """

        if (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                if self.detectFlag == True:
                    # 检测代码self.frame
                    self.label_num.setText("There are " + str(5) + " people.")

                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width
                q_image = QImage(frame.data, width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.label.width(), self.label.height())
                self.label.setPixmap(QPixmap.fromImage(q_image))
            else:
                self.cap.release()
                self.timer_camera.stop()  # 停止计时器
            
    def play(self):

        if path == '':
            reply = QtWidgets.QMessageBox.question(self, '提示',
                                                   "你选了个寂寞",
                                                   QtWidgets.QMessageBox.Yes)
            return
        with open("./filename.txt", 'w', encoding='utf-8') as f:
            f.truncate(0)
            print(f.write(str(path)))
        try:
            try:
                call('taskkill /F /IM play.exe')
            except:
                pass
            try:
                os.system('start play.exe')
                pass
            except Exception as e:
                print (e)

            #os.system('start play.exe')
        except:
            pass
        try:
            if self.cap != []:
                self.cap.release()
                self.timer_camera.stop()  # 停止计时器

            else:

                Warming = QMessageBox.warning(self, "Warming", "Push the left upper corner button to Quit.",
                                              QMessageBox.Yes)

        except:
            pass

    def close_wall(self):
        try:
            call('taskkill /F /IM play.exe')
        except:
            pass

    def close(self):
        MainWindow.hide()
        self.mini_icon.showMessage('动态壁纸', '动态壁纸已经最小化到系统托盘', QIcon('./2.ico'))


class MainWindow(QMainWindow):

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    def mousePressEvent(self, event):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = True
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = False

    def mousePressEvent(self, event):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = True
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = False

    def big(self):
        global big
        print('最大化：{}'.format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False

    def mini(self):

        self.showMinimized()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())