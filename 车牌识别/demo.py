import json
import requests
import base64

'''
车牌识别
'''

client_id = '5gDztMyRZKwIC72TGSZ9HA6s'
client_secret = 'IdHGx2oArRyQ30tSVW6R9sA3Su0ZiOnP'

# 获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        token_info = response.json()
        token_key = token_info['access_token']
    return token_key



request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
# 二进制方式打开图片文件
# f = open('./Test/京E51619.jpg', 'rb')
f = open('./Test/黑E99999.jfif', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = get_token()
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())