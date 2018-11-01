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
        html = res.text
        url = re.compile(r'<li style="float:left; width:135px;">.*?<a href="(.*?)">.*?</a>.*?</li>',re.DOTALL)
        urls = re.findall(url, html)
        num = 0
        for url in urls:
            num +=1
            res = requests.get(restart_url + url, headers=req_headers)
            if res.status_code == requests.codes.ok:
                html = res.text
                # 书名
                bookName = re.compile(r'<div id="maininfo">.*?<div id="bookdetail">.*?<div id="info">.*?<h1>(.*?)</h1>',re.DOTALL)
                bookName = re.findall(bookName,html)[0]
                print("爬取第" + str(num) + "本书")
                print("正在写入"+bookName)
                with open('梁羽生全集.txt', mode='a', encoding='utf-8') as f:
                    f.write('{bookName}\n'.format(bookName = bookName))
                    # 所有的章节
                    chapterName = re.compile(r'<dt>《'+ bookName +'》正文</dt>(.*?)</dl>',re.DOTALL)
                    chapterNames = re.findall(chapterName,html)
                    chapterName = re.compile(r'<dd> <a style="" href=".*?">(.*?)</a></dd>',re.DOTALL)
                    chapterNs = re.findall(chapterName, chapterNames[0])
                    # 章节链接
                    chapterUrl = re.compile(r'<dd> <a style="" href="(.*?)">.*?</a></dd>',re.DOTALL)
                    chapterUrls = re.findall(chapterUrl, chapterNames[0])
                    for i in range(len(chapterNs)):
                        f.write('{chapterName}\n'.format(chapterName=chapterNs[i]))
                        print("正在写入"+ chapterNs[i])
                        res = requests.get(restart_url + chapterUrls[i], headers=req_headers)
                        a = 0
                        while res.status_code != requests.codes.ok and a < 1:
                            res = requests.get(restart_url + chapterUrls[i], headers=req_headers)
                        if res.status_code == requests.codes.ok:
                            print(res.status_code)
                            html = res.text
                            # 章节内容
                            content = re.compile(r'</p>(.*?)<div align="center">',re.DOTALL)
                            content = re.findall(content,html)
                            for k in content:
                                content = re.sub(r'\r\n\t\t\t','', k)
                                content = re.sub(r'&nbsp;','', content)
                                content = re.sub(r'<br/><br/>', '\n ', content)
                                content = re.sub(r'&quot;', '"', content)
                                f.write('{content}\n'.format(content=''+ content))
                    f.write('\n\n\n')
        print("所有书籍爬取完毕,一共爬取"+ str(num) +"本书")

if __name__ == '__main__':
    start_url = 'https://www.liangyusheng.net/'
    crawl(start_url)