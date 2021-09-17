import pandas as pd
import numpy as np

chengyu = pd.read_json("idiom.json")
t = chengyu.pinyin.str.split()
chengyu["shoupin"] = t.str[0]
chengyu["weipin"] = t.str[-1]
chengyu = chengyu.set_index("word")[["shoupin", "weipin"]]

word = input("请输入一个成语：")
flag = True
if word not in chengyu.index:
    print("你输入的不是一个成语，程序结束！")
    flag = False
while flag:
    n = input("接龙的次数(1-100次的整数，输入任意字母表示结束程序)")
    if not n.isdigit():
        print("程序结束")
        break
    n = int(n)
    if not (0 < n <= 100):
        print("非法数字，程序结束")
        break
    for _ in range(n):
        words = chengyu.index[chengyu.shoupin == chengyu.loc[word, "weipin"]]
        if words.shape[0] == 0:
            print("没有找到可以接龙的成语，程序结束")
            flag = False
            break
        word = np.random.choice(words)
        print(word)