# -*- coding:utf-8 -*-
import re
import requests


def crawl(start_url):
    base_url = 'http://so.gushiwen.org'

    req_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    for i in range(1,126):

        restart_url = start_url + str(i) + '.aspx'
        print(restart_url)

        res = requests.get(restart_url, headers=req_headers)
        if res.status_code == requests.codes.ok:
            html = res.text

            # 获取所有诗的链接
            parttern_href = re.compile(r'<div class="cont">.*?<p><a .*? href="(.*?)" .*?>.*?</p>', flags=re.DOTALL)
            hrefs = re.findall(parttern_href, html)

            # 获取每一首诗的内容,并保存到本地
            with open('李白诗集.txt', mode='a', encoding='utf-8') as f:
                for href in hrefs:
                    href = base_url + href
                    res = requests.get(href, headers=req_headers)
                    if res.status_code == requests.codes.ok:
                        html = res.text
                        # 标题
                        parttern_title = re.compile(r'<div class="cont">.*?<h1 .*?>(.*?)</h1>', re.DOTALL)
                        title = re.search(parttern_title, html).group(1)
                        # 内容
                        parttern_content = re.compile(r'<div class="cont">.*?<div class="contson" id=".*?">(.*?)</div>',
                                                      re.DOTALL)
                        content = re.search(parttern_content, html).group(1)
                        content = re.sub(r'<br />', '\n', content)
                        content = re.sub(r'<p>', '', content)
                        content = re.sub(r'</p>', '', content)
                        print('正在获取 {title}'.format(title=title))
                        f.write('{title}{content}\n'.format(title=title, content=content))

if __name__ == '__main__':
    start_url = 'https://so.gushiwen.org/authors/authorvsw_b90660e3e492A'
    crawl(start_url)
