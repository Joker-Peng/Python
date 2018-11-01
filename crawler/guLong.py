#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests

def crawl(start_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    restart_url = start_url
    res = requests.get(restart_url, headers=req_headers)
    if res.status_code == requests.codes.ok:
        html = res.text.encode("latin1").decode("gbk")
        url = re.compile(r'<li><a class="tu" href="(.*?)">',re.DOTALL)
        urls = re.findall(url,html)
        for url in urls:
            res = requests.get(restart_url + url, headers=req_headers)
            if res.status_code == requests.codes.ok:
                # 开发该网站的编码居然是gb2312
                html = res.text.encode("latin1").decode("gbk")
                # 获取书名
                bookName = re.compile(r'<div class="fg">(.*?)</div>')
                bookName = re.findall(bookName,html)[0]
                with open('古龙全集.txt', mode='a', encoding='utf-8') as f:
                    f.write('{bookName}\n'.format(bookName = bookName))
                    print("正在写入" + bookName)

                    # 获取章节名
                    chapterName = re.compile(r'<li><a href=".*?">(.*?)</a></li>')
                    chapterNames = re.findall(chapterName,html)
                    # 获取章节链接
                    chapterUrl = re.compile(r'<a href="' + url + '(.*?).html">')
                    chapterUrls = re.findall(chapterUrl,html)
                    for i in range(len(chapterNames)):
                    # for i in range(1):
                        f.write('{chapterName}\n'.format(chapterName=re.sub(r'正文 ','',chapterNames[i])))
                        print("正在写入"+ chapterNames[i])
                        res = requests.get(restart_url + url + chapterUrls[i] + '.html', headers=req_headers)
                        if res.status_code == requests.codes.ok:
                            html = res.text.encode("latin1").decode("gbk")
                            content = re.compile(r'<p>(.*?)</p>')
                            contents = re.findall(content,html)
                            for content in contents:
                                content = re.sub(r'\u3000\u3000','',content)
                                content = re.sub(r'&quot;','"',content)
                                content = re.sub(r'&quot;','"',content)
                                content = re.sub(r'&hellip;&hellip;','... ...',content)
                                content = re.sub(r'&mdash;&mdash;','——---',content)
                                content = re.sub(r'&hellip;','...',content)
                                content = re.sub(r'<a .*?>.*?</a>','',content)
                                content = re.sub(r'<br /><br />','\n    ',content)
                                content = re.sub(r'&nbsp;','',content)
                                content = re.sub(r'&ldquo;','"',content)
                                content = re.sub(r'&rsquo;','"',content)
                                content = re.sub(r'&rdquo;','"',content)
                                content = re.sub(r'&lsquo;','"',content)
                                content = re.sub(r'【.*?】','',content)
                                f.write('{content}\n'.format(content='    ' + content))
                    f.write('\n\n\n')


if __name__ == '__main__':
    start_url = 'https://www.gulongwang.com'
    crawl(start_url)
