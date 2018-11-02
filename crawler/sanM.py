# -*- coding:utf-8 -*-

import requests
import re

def crawl(start_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get(start_url,req_headers)
    if res.status_code != requests.codes.ok:
        res = requests.get(start_url, req_headers)
    html = res.text.encode("latin1").decode("utf-8")
    # 创建文本文件
    # 获取作品链接
    url = re.compile(r'<h3><a href="(.*?)" target="_blank" title=".*?">.*?</a></h3>',re.DOTALL)
    urls = re.findall(url,html)
    # 作品的名字
    bookName = re.compile(r'<h3><a href=".*?" target="_blank" title=".*?">(.*?)</a></h3>',re.DOTALL)
    bookNames = re.findall(bookName,html)
    num = 0
    for u in range(len(urls)):
        num +=1
        res = requests.get(urls[u],req_headers)
        if res.status_code != requests.codes.ok:
            res = requests.get(urls[u], req_headers)
        html = res.text.encode("latin1").decode("utf-8")
        # 书名
        bookName = bookNames[u]
        with open('三毛全集.txt', mode='a', encoding='utf-8') as f:
            f.write('{bookName}\n\n'.format(bookName=''+ bookName))
            print("正在写入书本:" + bookName)
            print(num)
            # 获取章节名字和链接
            chapterUrl = re.compile(r'<li><a href="(.*?)" title=".*?">.*?</a></li>')
            chapterUrls = re.findall(chapterUrl,html)
            chapterName = re.compile(r'<li><a href=".*?" title=".*?">(.*?)</a></li>')
            chapterNames = re.findall(chapterName,html)
            for l in range(len(chapterUrls)):
                res = requests.get(chapterUrls[l])
                if res.status_code != requests.codes.ok:
                    res = requests.get(chapterUrls[l])
                html = res.text.encode("latin1").decode("utf-8")
                # 章节名
                chapterName = chapterNames[l]
                f.write('{chapterName}\n'.format(chapterName='' + chapterName))
                # 章节内容
                content = re.compile(r'<div id="htmlContent" class="contentbox">.*?<p>(.*?)</p>',re.DOTALL)
                content = re.findall(content,html)
                content = re.sub(r'&mdash;','—',content[0])
                content = re.sub(r'<br />\r\n<br />','\n',content)
                content = re.sub(r'&mdash;','—',content)
                content = re.sub(r'&nbsp;',' ',content)
                content = re.sub(r'&rdquo;','"',content)
                content = re.sub(r'&ldquo;','"',content)
                content = re.sub(r'<br />','\n',content)
                f.write('{content}\n\n'.format(content='' + content))
            f.write('\n\n\n\n')
    print(num)


if __name__ == "__main__":
    start_url = 'http://sanmao.zuopinj.com/'
    crawl(start_url)