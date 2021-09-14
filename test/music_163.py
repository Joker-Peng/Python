import requests                        # 用于获取网页内容的模块
from bs4 import BeautifulSoup        # 用于解析网页源代码的模块
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def handle_hmtl(search_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    link = "https://music.163.com/#/search/m/?s=" + search_name + "&type=1"  # 要搜索的链接
    driver.get(link)
    iframe_elemnt = driver.find_element_by_id("g_iframe")  # 因为直接获取不到iframe的内容，因此使用web_driver
    driver.switch_to.frame(iframe_elemnt)  # 关键步骤，跳转到iframe里面，就可以获取HTML内容
    soup = BeautifulSoup(driver.page_source, "html.parser")  # 通过 BeautifulSoup 模块解析网页，具体请参考官方文档。
    L = []  # 存储结果的列表
    nu = 0
    for value in soup.select(
            "div[class='srchsongst'] div[class^='item f-cb h-flag']"):  # 获取到关键class：srchsongst下面的所有元素，结果是一个列表，使用的是CSS的方式
        D = {'num': 'null', 'name': 'null', 'id': 'null', 'singer': 'null', 'song_sheet': 'null'}  # 初始化字典
        D['num'] = nu  # 用来计算num
        D['name'] = value.b.attrs['title']  # 歌名
        D['id'] = value.a.attrs['data-res-id']  # 歌曲ID
        D['singer'] = '/'.join([i.string for i in value.select('a[href^="/artist?i"]')])  # 歌唱者
        D['song_sheet'] = value.select('a[class^="s-fc3"]')[0].attrs['title']  # 专辑
        L.append(D)
        nu += 1
    return L


def load_song(num, result):
    """
    result 是一个列表
    num 是一个str
    """
    if isinstance(int(num), int):
        num = int(num)
        if num >= 0 and num <= len(result):
            song_id = result[num]['id']
            song_down_link = "http://music.163.com/song/media/outer/url?id=" + result[num]['id'] + ".mp3"  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
            print("歌曲正在下载...")
            response = requests.get(song_down_link, headers=headers).content  # 亲测必须要加 headers 信息，不然获取不了。
            f = open(result[num]['name'] + ".mp3", 'wb')  # 以二进制的形式写入文件中
            f.write(response)
            f.close()
            print("下载完成.\n\r")
        else:
            print("你输入的数字不在歌曲列表范围，请重新输入")
    else:
        print("请输入正确的歌曲序号")


if __name__ == '__main__':
    headers={    # 伪造浏览器头部，不然获取不到网易云音乐的页面源代码。
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Referer':'http://93.174.95.27',
    }
    search_name = input("请输入你想要在网易云音乐中搜索的单曲：")
    result = handle_hmtl(search_name)
    print("%3s %-35s %-20s %-20s " % ("序号", "  歌名", "歌手", "专辑"))
    for i in range(len(result)):
        print("%3s %-35s %-20s %-20s " % (
        result[i]["num"], result[i]["name"], result[i]["singer"], result[i]["song_sheet"]))
    num = input("请输入你想要下载歌曲的序号/please input the num you want to download：")
    load_song(num, result)  # 下载歌曲