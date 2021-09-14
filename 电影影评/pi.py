# 导入Pie组件，用于生成饼图
from pyecharts.charts import Pie
from pyecharts import options as opts

# 获取评论中所有评分
rates = []
with open('中国医生.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        try:
            rates.append(row.split(',')[4])
        except:
            pass

# print(rates)

# 定义星级，并统计各星级评分数量
attr = ['五星', '四星', '三星', '二星', '一星']
value = [
    rates.count('5.0') + rates.count('4.5'),
    rates.count('4.0') + rates.count('3.5'),
    rates.count('3.0') + rates.count('2.5'),
    rates.count('2.0') + rates.count('1.5'),
    rates.count('1.0') + rates.count('0.5')
]
# print(value)

pie = (
    Pie()
    .add("", [list(z) for z in zip(attr, value)])
    .set_global_opts(title_opts=opts.TitleOpts(title="《中国医生》评分比例饼图"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
)
pie.render('评分.html')

