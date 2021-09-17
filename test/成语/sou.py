from gooey import Gooey, GooeyParser
import pandas as pd

chengyu = pd.read_json("idiom.json")
t = chengyu.pinyin.str.split()
chengyu["shoupin"] = t.str[0]
chengyu["weipin"] = t.str[-1]
chengyu = chengyu.set_index("word")[["shoupin", "weipin"]]


@Gooey
def main():
    parser = GooeyParser(description="成语接龙查询器 - @小小明")
    parser.add_argument('word', help="被查询的成语")
    args = parser.parse_args()
    word = args.word
    if word not in chengyu.index:
        print("你输入的不是一个成语，请重新输入！")
    else:
        words = chengyu.index[chengyu.shoupin == chengyu.loc[word, "weipin"]]
        if words.shape[0] > 0:
            print("满足条件的成语有：")
            print("、".join(words))
        else:
            print("抱歉，没有找到能够满足条件的成语")
        print("-----" * 10)


if __name__ == '__main__':
    main()