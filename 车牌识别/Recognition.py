# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import json
import time
import requests
import base64


class PlateRecognition():
    client_id = ''
    client_secret = ''
    def __init__(self):
        self.MAX_WIDTH = 1000  # 原始图片最大宽度
        self.Min_Area = 2000  # 车牌区域允许最大面积
        self.PROVINCE_START = 1000

        # 省份代码保存在provinces.json中
        with open('provinces.json', 'r', encoding='utf-8') as f:
            self.provinces = json.load(f)

        # 车牌类型保存在cardtype.json中，便于调整
        with open('cardtype.json', 'r', encoding='utf-8') as f:
            self.cardtype = json.load(f)

        # 字母所代表的地区保存在Prefecture.json中，便于更新
        with open('Prefecture.json', 'r', encoding='utf-8') as f:
            self.Prefecture = json.load(f)

        # 车牌识别的部分参数保存在js中，便于根据图片分辨率做调整
        f = open('config.js')
        j = json.load(f)
        for c in j["config"]:
            if c["open"]:
                self.cfg = c.copy()
                break

    def __del__(self):
        pass

    # 读取图片文件
    def __imreadex(self, filename):
        return cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_COLOR)

    def __point_limit(self, point):
        if point[0] < 0:
            point[0] = 0
        if point[1] < 0:
            point[1] = 0


    def accurate_place(self, card_img_hsv, limit1, limit2, color):
        row_num, col_num = card_img_hsv.shape[:2]
        xl = col_num
        xr = 0
        yh = 0
        yl = row_num
        # col_num_limit = self.cfg["col_num_limit"]
        row_num_limit = self.cfg["row_num_limit"]
        col_num_limit = col_num * 0.8 if color != "green" else col_num * 0.5  # 绿色有渐变
        for i in range(row_num):
            count = 0
            for j in range(col_num):
                H = card_img_hsv.item(i, j, 0)
                S = card_img_hsv.item(i, j, 1)
                V = card_img_hsv.item(i, j, 2)
                if limit1 < H <= limit2 and 34 < S and 46 < V:
                    count += 1
            if count > col_num_limit:
                if yl > i:
                    yl = i
                if yh < i:
                    yh = i
        for j in range(col_num):
            count = 0
            for i in range(row_num):
                H = card_img_hsv.item(i, j, 0)
                S = card_img_hsv.item(i, j, 1)
                V = card_img_hsv.item(i, j, 2)
                if limit1 < H <= limit2 and 34 < S and 46 < V:
                    count += 1
            if count > row_num - row_num_limit:
                if xl > j:
                    xl = j
                if xr < j:
                    xr = j
        return xl, xr, yh, yl

    # 预处理
    def pretreatment(self, car_pic):
        if type(car_pic) == type(""):
            img = self.__imreadex(car_pic)
        else:
            img = car_pic
        pic_hight, pic_width = img.shape[:2]

        if pic_width > self.MAX_WIDTH:
            resize_rate = self.MAX_WIDTH / pic_width
            img = cv2.resize(img, (self.MAX_WIDTH, int(pic_hight * resize_rate)),
                             interpolation=cv2.INTER_AREA)  # 图片分辨率调整
        # cv2.imshow('Image', img)

        blur = self.cfg["blur"]
        # 高斯去噪
        if blur > 0:
            img = cv2.GaussianBlur(img, (blur, blur), 0)
        oldimg = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('GaussianBlur', img)

        kernel = np.ones((20, 20), np.uint8)
        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  # 开运算
        img_opening = cv2.addWeighted(img, 1, img_opening, -1, 0);  # 与上一次开运算结果融合
        # cv2.imshow('img_opening', img_opening)

        # 找到图像边缘
        ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化
        img_edge = cv2.Canny(img_thresh, 100, 200)
        # cv2.imshow('img_edge', img_edge)

        # 使用开运算和闭运算让图像边缘成为一个整体
        kernel = np.ones((self.cfg["morphologyr"], self.cfg["morphologyc"]), np.uint8)
        img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)  # 闭运算
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)  # 开运算
        # cv2.imshow('img_edge2', img_edge2)

        # cv2.imwrite('./edge2.png', img_edge2)

        # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
        image, contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.Min_Area]
        # print(contours[0])

        # 逐个排除不是车牌的矩形区域
        car_contours = []
        for cnt in contours:
            # 框选 生成最小外接矩形 返回值（中心(x,y), (宽,高), 旋转角度）
            rect = cv2.minAreaRect(cnt)
            # print('宽高:',rect[1])
            area_width, area_height = rect[1]
            # 选择宽大于高的区域
            if area_width < area_height:
                area_width, area_height = area_height, area_width
            wh_ratio = area_width / area_height
            # print('宽高比：',wh_ratio)
            # 要求矩形区域长宽比在2到5.5之间，2到5.5是车牌的长宽比，其余的矩形排除
            if wh_ratio > 2 and wh_ratio < 5.5:
                car_contours.append(rect)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
            # 框出所有可能的矩形
            # oldimg = cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            # cv2.imshow("Test",oldimg )
            # print(car_contours)

        # 矩形区域可能是倾斜的矩形，需要矫正，以便使用颜色定位
        card_imgs = []
        for rect in car_contours:
            if rect[2] > -1 and rect[2] < 1:  # 创造角度，使得左、高、右、低拿到正确的值
                angle = 1
            else:
                angle = rect[2]
            rect = (rect[0], (rect[1][0] + 5, rect[1][1] + 5), angle)  # 扩大范围，避免车牌边缘被排除
            box = cv2.boxPoints(rect)
            heigth_point = right_point = [0, 0]
            left_point = low_point = [pic_width, pic_hight]
            for point in box:
                if left_point[0] > point[0]:
                    left_point = point
                if low_point[1] > point[1]:
                    low_point = point
                if heigth_point[1] < point[1]:
                    heigth_point = point
                if right_point[0] < point[0]:
                    right_point = point

            if left_point[1] <= right_point[1]:  # 正角度
                new_right_point = [right_point[0], heigth_point[1]]
                pts2 = np.float32([left_point, heigth_point, new_right_point])  # 字符只是高度需要改变
                pts1 = np.float32([left_point, heigth_point, right_point])
                M = cv2.getAffineTransform(pts1, pts2)
                dst = cv2.warpAffine(oldimg, M, (pic_width, pic_hight))
                self.__point_limit(new_right_point)
                self.__point_limit(heigth_point)
                self.__point_limit(left_point)
                card_img = dst[int(left_point[1]):int(heigth_point[1]), int(left_point[0]):int(new_right_point[0])]
                card_imgs.append(card_img)

            elif left_point[1] > right_point[1]:  # 负角度

                new_left_point = [left_point[0], heigth_point[1]]
                pts2 = np.float32([new_left_point, heigth_point, right_point])  # 字符只是高度需要改变
                pts1 = np.float32([left_point, heigth_point, right_point])
                M = cv2.getAffineTransform(pts1, pts2)
                dst = cv2.warpAffine(oldimg, M, (pic_width, pic_hight))
                self.__point_limit(right_point)
                self.__point_limit(heigth_point)
                self.__point_limit(new_left_point)
                card_img = dst[int(right_point[1]):int(heigth_point[1]), int(new_left_point[0]):int(right_point[0])]
                card_imgs.append(card_img)
        # cv2.imshow("card", card_imgs[0])

        # #____开始使用颜色定位，排除不是车牌的矩形，目前只识别蓝、绿、黄车牌
        colors = []
        for card_index, card_img in enumerate(card_imgs):
            green = yellow = blue = black = white = 0
            try:
                # 有转换失败的可能，原因来自于上面矫正矩形出错
                card_img_hsv = cv2.cvtColor(card_img, cv2.COLOR_BGR2HSV)
            except:
                print('BGR转HSV失败')
                card_imgs = colors = None
                return card_imgs, colors

            if card_img_hsv is None:
                continue
            row_num, col_num = card_img_hsv.shape[:2]
            card_img_count = row_num * col_num

            # 确定车牌颜色
            for i in range(row_num):
                for j in range(col_num):
                    H = card_img_hsv.item(i, j, 0)
                    S = card_img_hsv.item(i, j, 1)
                    V = card_img_hsv.item(i, j, 2)
                    if 11 < H <= 34 and S > 34:  # 图片分辨率调整
                        yellow += 1
                    elif 35 < H <= 99 and S > 34:  # 图片分辨率调整
                        green += 1
                    elif 99 < H <= 124 and S > 34:  # 图片分辨率调整
                        blue += 1

                    if 0 < H < 180 and 0 < S < 255 and 0 < V < 46:
                        black += 1
                    elif 0 < H < 180 and 0 < S < 43 and 221 < V < 225:
                        white += 1
            color = "no"
            # print('黄：{:<6}绿：{:<6}蓝：{:<6}'.format(yellow,green,blue))

            limit1 = limit2 = 0
            if yellow * 2 >= card_img_count:
                color = "yellow"
                limit1 = 11
                limit2 = 34  # 有的图片有色偏偏绿
            elif green * 2 >= card_img_count:
                color = "green"
                limit1 = 35
                limit2 = 99
            elif blue * 2 >= card_img_count:
                color = "blue"
                limit1 = 100
                limit2 = 124  # 有的图片有色偏偏紫
            elif black + white >= card_img_count * 0.7:
                color = "bw"
            # print(color)
            colors.append(color)
            # print(blue, green, yellow, black, white, card_img_count)
            if limit1 == 0:
                continue

            # 根据车牌颜色再定位，缩小边缘非车牌边界
            xl, xr, yh, yl = self.accurate_place(card_img_hsv, limit1, limit2, color)
            if yl == yh and xl == xr:
                continue
            need_accurate = False
            if yl >= yh:
                yl = 0
                yh = row_num
                need_accurate = True
            if xl >= xr:
                xl = 0
                xr = col_num
                need_accurate = True
            card_imgs[card_index] = card_img[yl:yh, xl:xr] \
                if color != "green" or yl < (yh - yl) // 4 else card_img[yl - (yh - yl) // 4:yh, xl:xr]
            if need_accurate:  # 可能x或y方向未缩小，需要再试一次
                card_img = card_imgs[card_index]
                card_img_hsv = cv2.cvtColor(card_img, cv2.COLOR_BGR2HSV)
                xl, xr, yh, yl = self.accurate_place(card_img_hsv, limit1, limit2, color)
                if yl == yh and xl == xr:
                    continue
                if yl >= yh:
                    yl = 0
                    yh = row_num
                if xl >= xr:
                    xl = 0
                    xr = col_num
            card_imgs[card_index] = card_img[yl:yh, xl:xr] \
                if color != "green" or yl < (yh - yl) // 4 else card_img[yl - (yh - yl) // 4:yh, xl:xr]
        # cv2.imshow("result", card_imgs[0])
        # cv2.imwrite('1.jpg', card_imgs[0])
        # print('颜色识别结果：' + colors[0])
        return card_imgs, colors


    def get_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.client_id + '&client_secret=' + self.client_secret
        response = requests.get(host)
        if response:
            token_info = response.json()
            token_key = token_info['access_token']
        return token_key


    def get_license_plate(self, car_pic):
        result = {}
        card_imgs, colors = self.pretreatment(car_pic)
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        # 二进制方式打开图片文件
        f = open(car_pic, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        access_token = self.get_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            license_result = response.json()['words_result']['number']
            card_color = response.json()['words_result']['color']
            if license_result != []:
                result['InputTime'] = time.strftime("%Y-%m-%d %H:%M:%S")
                result['Type'] = self.cardtype[card_color]
                result['Picture'] = card_imgs[0]
                result['Number'] = ''.join(license_result[:2]) + '·' + ''.join(license_result[2:])
                try:
                    result['From'] = ''.join(self.Prefecture[license_result[0]][license_result[1]])
                except:
                    result['From'] = '未知'
                return result
        else:
            return None



# 测试
if __name__ == '__main__':
    c = PlateRecognition()
    # card_imgs, colors = c.pretreatment('./2.jpg')
    result = c.get_license_plate('./2.jpg')
    # cv2.imshow('card', card_imgs)

    cv2.waitKey(0)
