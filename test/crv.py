from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 引入自定义模块
import dc
# 引入内置模块
import sys
import os
# 引入第三方模块
import requests, base64
from PIL import Image


class parentWindow(QWidget, dc.Ui_Form):
    # 初始化方法
    def __init__(self):
        # 找到父类 首页面
        super(parentWindow, self).__init__()
        # 初始化页面方法
        self.setupUi(self)
        # 点击选择图片
        self.selectImg.clicked.connect(self.openfile)
        # 点击查看图片
        self.viewImg.clicked.connect(self.viewbtn)

    # 选择图片执行方法
    def openfile(self):
        # 启动选择文件对话空，查找jpg以及png图片
        self.download_path = QFileDialog.getOpenFileName(self, "选择要识别的图片", os.getcwd(), "Image Files(*.jpg *.png)")
        # 判断是否选择图片
        if not self.download_path[0].strip():
            QMessageBox.information(self, '提示信息', '没有选择名片图片')
            pass
        else:
            # pixmap解析图片
            pixmap = QPixmap(self.download_path[0])
            # 设置图片
            self.imgLabel.setPixmap(pixmap)
            # 让图片自适应label大小
            self.imgLabel.setScaledContents(True)
            try:
                # 识别名片图片返回识别结果
                content = self.recgImg()
            except:
                QMessageBox.information(self, '提示信息', '识别错误请重新选择图片')

            # 识别图片的数据赋值
            words_result = content['words_result']
            # print(words_result)
            text = ''
            for item in words_result:
                for v in item.values():
                    text = text + '\n' + v
            self.discernText.setText(text)

    # 识别名片图片
    def recgImg(self):
        # 获取baiduToken
        apikey = '5gDztMyRZKwIC72TGSZ9HA6s'
        seckey = 'IdHGx2oArRyQ30tSVW6R9sA3Su0ZiOnP'
        tokenUrl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + apikey + '&client_secret=' + seckey
        res = requests.get(url=tokenUrl, headers={'content-type': 'application/json; charset=UTF-8'}).json()
        baiduToken = res['access_token']

        '''
        图片识别（API）
        '''
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
        # 二进制方式打开图片文件
        f = open(self.download_path[0], 'rb')
        img = base64.b64encode(f.read())

        params = {"image": img}
        # access_token = '[调用鉴权接口获取的token]'
        request_url = request_url + "?access_token=" + baiduToken
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # print(response.json())
            return response.json()

    # 点击查看图片显示大图功能
    def viewbtn(self):
        if self.download_path:
            # 使用电脑中的看图工具打开图片
            img = Image.open(self.download_path[0])
            # 显示图片
            img.show()
        else:
            QMessageBox.information(self, '提示信息', '先选择名片图片')


if __name__ == '__main__':
    # 每一个PyQt5应用都必须创建一个应用对象
    app = QApplication(sys.argv)
    # 初始化页面
    window = parentWindow()
    # 显示首页
    window.show()
    sys.exit(app.exec_())
