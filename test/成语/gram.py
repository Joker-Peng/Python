import pandas as pd
import numpy as np

chengyu = pd.read_json("idiom.json")
t = chengyu.pinyin.str.split()
chengyu["shoupin"] = t.str[0]
chengyu["weipin"] = t.str[-1]
chengyu = chengyu.set_index("word")[["shoupin", "weipin"]]

is_head = input("是否先手(输入N表示后手，其他表示先手)")
if is_head == "N":
    word2 = np.random.choice(chengyu.index)
    print(word2)
    weipin = chengyu.loc[word2, "weipin"]
else:
    weipin = ''
while True:
    word = input("请输入一个成语（认输或离开请按Q）：")
    if word == "Q":
        print("你离开了游戏，再见！！！")
        break
    if word not in chengyu.index:
        print("你输入的不是一个成语，请重新输入！")
        continue
    if weipin and chengyu.loc[word, 'shoupin'] != weipin:
        print("你输入的成语并不能与机器人出的成语接上来，你输了，游戏结束！！！")
        break
    words = chengyu.index[chengyu.shoupin == chengyu.loc[word, "weipin"]]
    if words.shape[0] == 0:
        print("恭喜你赢了！成语机器人已经被你打败！！！")
        break
    word2 = np.random.choice(words)
    print(word2)
    weipin = chengyu.loc[word2, "weipin"]