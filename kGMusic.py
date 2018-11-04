import requests
import json
import re

''' 原贴地址: https://blog.csdn.net/qq_40925239/article/details/82749421 '''


def get_song(x):
    url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407470964083509348_1534929985284&keyword={}&" \
          "page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filte" \
          "r=0&_=1534929985286".format(x)
    res = requests.get(url).text
    js = json.loads(res[res.index('(') + 1:-2])
    data = js['data']['lists']
    for i in range(10):
        print(str(i + 1) + ">>>" + str(data[i]['FileName']).replace('<em>', '').replace('</em>', ''))
    number = int(input("\n请输入要下载的歌曲序号（输入-1退出程序）: "))
    if number == -1:
        exit()
    else:
        name = str(data[number - 1]['FileName']).replace('<em>', '').replace('</em>', '')
        fhash = re.findall('"FileHash":"(.*?)"', res)[number - 1]
        hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + fhash
        hash_content = requests.get(hash_url)
        play_url = ''.join(re.findall('"play_url":"(.*?)"', hash_content.text))
        real_download_url = play_url.replace("\\", "")
        with open(name + ".mp3", "wb")as fp:
            fp.write(requests.get(real_download_url).content)
        print("歌曲已下载完成！")


if __name__ == '__main__':
    x = input("请输入歌名：")
    get_song(x)