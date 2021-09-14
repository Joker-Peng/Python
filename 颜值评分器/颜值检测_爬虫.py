import requests
import parsel


# 1.找到数据所在url地址（系统分析网页性质）
url = "https://www.huya.com/g/2168"
headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

# 2. 发送网络请求
response = requests.get(url=url, headers=headers)
html_data = response.text
# print(html_data)

# 3. 数据解析
selector = parsel.Selector(html_data)
lis = selector.xpath('//li[@class="game-live-item"]')  # 所有li标签

for li in lis:
    img_name = li.xpath('.//span[@class="avatar fl"]/i/text()').get()  # 主播名字
    img_url = li.xpath('.//a/img/@data-original').get()  # 主播图片地址
    # print(img_name, img_url)

    # 请求图片数据
    img_data = requests.get(url=img_url).content  # 图片数据

    # 4. 数据保存
    # 准备文件名
    file_name = img_name + '.jpg'
    with open('img\\' + file_name, mode='wb') as f:
        f.write(img_data)
        print('正在保存:', file_name)




