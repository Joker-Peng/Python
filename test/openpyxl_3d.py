from openpyxl import Workbook
from openpyxl.chart import (
    Reference,
    Series,
    BarChart3D,
)
# 生成3D图
wb = Workbook()
ws = wb.active

rows = [
    (None,2013,2014,2015,2016,2017,2018),
    ("Apples",5,4,6,7,8,9),
    ("Oranges",6,2,3,4,5,6),
    ("Pears",8,3,5,6,7,9)
]

for row in rows:
    ws.append(row)

data1 = Reference(ws, min_col=2, min_row=1, max_col=7, max_row=4)
titles = Reference(ws, min_col=1, min_row=2, max_row=4)
chart = BarChart3D()
chart.title = "3D Bar Chart1"
chart.add_data(data=data1, titles_from_data=True)
chart.set_categories(titles)

ws.add_chart(chart, "A6")


wb.save("bar3d.xlsx")