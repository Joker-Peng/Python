import os
from face_api import face_input


path = './img'
img_list = os.listdir(path)
# print(img_list)
score_dict ={}

for img in img_list:
    try:
        # 提取主播名字
        name = img.split('.')[0]
        # print(name)
        # 构建图片路径
        img_path = path + '//' + img
        # 调用颜值检测接口
        face_score = face_input(img_path)
        # print(face_score)
        score_dict[name] = face_score
    except:
        pass
        # print(f'正在检测{name}| 检测失败')
    else:
        print(f'正在检测{name}| \t\t 颜值打分为：{face_score}')

print('\n================检测完成==================')

sorted_score = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
# print(sorted_score)

for i, j in enumerate(sorted_score):
    print(f'小姐姐名字是：{sorted_score[i][0]} | 颜值名次是：第{i+1}名 | 颜值分数是：{sorted_score[i][1]}')

