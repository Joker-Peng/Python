import mammoth
from markdownify import markdownify
import time
from pathlib import Path
import os
# 支持word中存在图片转html文件
def wordToHtml(filename):
    with open(filename+".docx", "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        with open(filename+".html", "w") as html_file:
            html_file.write(result.value)

# 不支持word中存在图片转md文件
def wordToMd(filename):
    with open(filename+".docx", "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        with open(filename+".md", "w") as markdown_file:
            markdown_file.write(result.value)

# 支持word中存在图片转md文件
def HtmlMD(filename):
    with open(filename+".docx", "rb") as docx_file:
        # 转化Word文档为HTML
        result = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.img_element(convert_img))
        # 获取HTML内容
        html = result.value
        # 转化HTML为Markdown
        md = markdownify(html, heading_style="ATX")
        with open("./docx_to_html.html", 'w', encoding='utf-8') as html_file,open("docx_to_md.md", "w", encoding='utf-8') as md_file:
            # html_file.write(html)
            md_file.write(md)
        messages = result.messages

# 转存Word文档内的图片
def convert_img(image):
    with image.open() as image_bytes:
        file_suffix = image.content_type.split("/")[1]
        my_img = Path("../img")
        if my_img.is_dir()==0:
            os.makedirs("../img")
        path_file = "./img/{}.{}".format(str(time.time()),file_suffix)
        with open(path_file, 'wb') as f:
            f.write(image_bytes.read())
    return {"src":path_file}

if __name__ == '__main__':
    # wordToHtml("test")
    # wordToMd("test")
    HtmlMD("test")