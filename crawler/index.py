# 测试自动打开浏览器
# from selenium import webdriver 
# browser = webdriver.Chrome() # 打开谷歌浏览器
# browser = webdriver.Firefox()  # 打开火狐浏览器
# browser = webdriver. PhantomJS() # 无界面浏览器
# browser.get('https://www.baidu.com') 
# print(browser.current_url)

# 测试直接解析xml插件
# from bs4 import BeautifulSoup
# soup = BeautifulSoup('<p>Hello</p>','lxml')
# print(soup.p.string) 

# 测试 OCR
import tesserocr
from PIL import Image

image = Image.open('image.png')
print(tesserocr.image_to_text(image))
