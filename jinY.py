# -*- coding:utf-8 -*-
import re
import requests

def crawl(start_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    restart_url = start_url
    base_url = 'http://www.jinyongwang.com'
    res = requests.get(restart_url, headers=req_headers)
    if res.status_code == requests.codes.ok:
        html = res.text
        url = re.compile(r'<p class="img pu_bookrotate"><a href="(.*?)">',re.DOTALL)
        urls = re.findall(url, html)
        urls = urls[15:30]
        for url in urls:
            res = requests.get(base_url + url, headers=req_headers)
            if res.status_code == requests.codes.ok:
                html = res.text
                # 书名
                bookName = re.compile(r'span class="navon navcen"><a href="/"><i class="icon">&#xe63d;</i></a> · (.*?)</span>',re.DOTALL)
                bookName = re.findall(bookName,html)[0]
                print("正在写入"+bookName)
                with open('金庸全集.txt', mode='a', encoding='utf-8') as f:
                    f.write('{bookName}\n'.format(bookName = bookName))
                    # 所有的章节
                    chapterName = re.compile(r'<li><a href="'+ url + '.*?">(.*?)</a></li>',re.DOTALL)
                    chapterNames = re.findall(chapterName,html)
                    # 所有章节的链接
                    chapterUrl = re.compile(r'<li><a href="'+ url + '(.*?)">.*?</a></li>',re.DOTALL)
                    chapterUrls = re.findall(chapterUrl,html)
                    for i in range(len(chapterNames)):
                        f.write('{chapterName}\n'.format(chapterName=chapterNames[i]))
                        print("正在写入"+ chapterNames[i])
                        res = requests.get(base_url + url + chapterUrls[i], headers=req_headers)
                        if res.status_code == requests.codes.ok:
                            html = res.text
                            # 章节的内容
                            content = re.compile(r'<p>(.*?)<p>',re.DOTALL)
                            content = re.findall(content,html)
                            for k in content:
                                f.write('{content}\n'.format(content='    '+k))
                    f.write('\n\n\n')


if __name__ == '__main__':
    start_url = 'http://www.jinyongwang.com/book'
    crawl(start_url)
