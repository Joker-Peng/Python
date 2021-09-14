import base64
import requests
import pprint


# 获取token
def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = 'aR6Oytn7ycDyhjBqPYCAGgqh'
    # client_id = '5gDztMyRZKwIC72TGSZ9HA6s'
    client_secret = 'dXjz8QELSaj238GuEr0I3xnarEurWhit' #'IdHGx2oArRyQ30tSVW6R9sA3Su0ZiOnP'
    # client_secret = 'IdHGx2oArRyQ30tSVW6R9sA3Su0ZiOnP' #'IdHGx2oArRyQ30tSVW6R9sA3Su0ZiOnP'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        # print(response.json())
        return response.json()['access_token']


# 颜值检测接口
def face_input(file_path):
    with open(file_path, 'rb') as file:
        data = base64.b64encode(file.read())
    img = data.decode()
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    params = "{\"image\":\"%s\",\"image_type\":\"BASE64\",\"face_field\":\"beauty\"}" % img
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        beauty = response.json()['result']['face_list'][0]['beauty']
        # pprint.pprint(response.json())
        return beauty
        # print(response.json())

if __name__ == '__main__':
    print(face_input(r'wo.jpg'))






