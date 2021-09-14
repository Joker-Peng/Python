import requests
import ssl, json
from datetime import datetime, timedelta
import time

#
# 获取数据，根据url获取
def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36',
           }
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    # print(html_data)
    return html_data


# 处理数据
def parse_data(html):
    data = json.loads(html)['cmts']  # 将str转换为json
    comments = []
    for item in data:
        comment = {
            'id': item['id'],
            'nickName': item['nickName'],
            'cityName': item['cityName'] if 'cityName' in item else '',  # 处理cityName不存在的情况
            'content': item['content'].replace('\n', ' ', 10),  # 处理评论内容换行的情况
            'score': item['score'],
            'startTime': item['startTime']
        }
        comments.append(comment)
    return comments


# 存储数据，存储到文本文件
def save_to_txt():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间，从当前时间向前获取
    end_time = '2021-07-09 00:00:00'
    while start_time > end_time:
        url = 'https://m.maoyan.com/mmdb/comments/movie/1337700.json?_v_=yes&offset=0&startTime=' + start_time.replace(' ', '%20')
        html = None
        '''
            问题：当请求过于频繁时，服务器会拒绝连接，实际上是服务器的反爬虫策略
            解决：1.在每个请求间增加延时0.1秒，尽量减少请求被拒绝
                 2.如果被拒绝，则0.5秒后重试
        '''
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)

        comments = parse_data(html)
        print(comments)
        start_time = comments[14]['startTime']  # 获得末尾评论的时间
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str

        for item in comments:
            with open('中国医生.txt', 'a', encoding='utf-8') as f:
                f.write(str(item['id'])+','+item['nickName'] + ',' + item['cityName'] + ',' + item['content'] + ',' + str(item['score'])+ ',' + item['startTime'] + '\n')


if __name__ == '__main__':
    # html = get_data('http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=0&startTime=2021-07-14%2022%3A25%3A03')
    # print(html)
    save_to_txt()
