## 导入相关包
import requests
import random
import time
import csv
import re
from fake_useragent import UserAgent  # 随机生成UserAgent
from lxml import etree  # xpath解析

## 创建文件对象
f = open('中国医生.csv', 'w', encoding='utf-8-sig', newline="")
csv_write = csv.DictWriter(f, fieldnames=['评论者', '评分等级', '评论日期', '点赞数', '评论内容'])
csv_write.writeheader()  # 写入文件头

## 设置请求头参数：User-Agent, cookie, referer
headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

# https://movie.douban.com/subject/35087699/comments?start={page}&limit=20&status=P&sort=new_score
## 循环爬取25页短评，每页短评20条，共400条短评
for i in range(25):
    url = 'https://movie.douban.com/subject/35087699/comments?start={}&limit=20&status=P&sort=new_score'.format(i * 20)
    # request请求获取网页页面
    page_text = requests.get(url=url, headers=headers).text
    # etree解析HTML文档
    tree = etree.HTML(page_text)

    # 获取评论者字段
    reviewer = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/a/text()")
    # 获取评分等级字段
    score = tree.xpath("//div[@class='comment-item ']//span[@class='comment-info']/span[2]/@title")
    # 获取评论日期字段
    comment_date = tree.xpath("//div[@class='comment-item ']//span[@class='comment-time ']/text()")
    # 获取点赞数字段
    vote_count = tree.xpath("//div[@class='comment-item ']//span[@class='votes vote-count']/text()")
    # 获取评论内容字段
    comments = tree.xpath("//p[@class=' comment-content']/span/text()")

    # 去除评论日期的换行符及空格
    comment_date = list(map(lambda date: re.sub('\s+', '', date), comment_date))  # 去掉换行符制表符
    comment_date = list(filter(None, comment_date))  # 去掉上一步产生的空元素

    # 由于每页20条评论，故需循环20次依次将获取到的字段值写入文件中
    for j in range(20):
        data_dict = {'评论者': reviewer[j], '评分等级': score[j], '评论日期': comment_date[j], '点赞数': vote_count[j],
                     '评论内容': comments[j]}
        csv_write.writerow(data_dict)

    print('第{}页爬取成功'.format(i + 1))

    # 设置睡眠时间间隔，防止频繁访问网站
    time.sleep(random.randint(5, 10))

print("---------------")
print("所有评论爬取成功")
