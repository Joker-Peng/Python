# -*- coding:utf-8 -*-

import xlsxwriter
# 生成饼状图

# 创建一个excel
workbook = xlsxwriter.Workbook("chart_pie.xlsx")
# 创建一个sheet
worksheet = workbook.add_worksheet()

# 自定义样式，加粗
bold = workbook.add_format({'bold': 1})

# --------1、准备数据并写入excel---------------
# 向excel中写入数据，建立图标时要用到
data = [
    ['closed', 'active', 'reopen', 'NT'],
    [1012, 109, 123, 131],
]

# 写入数据
worksheet.write_row('A1', data[0], bold)
worksheet.write_row('A2', data[1])

# --------2、生成图表并插入到excel---------------
# 创建一个柱状图(pie chart)
chart_col = workbook.add_chart({'type': 'pie'})

# 配置第一个系列数据
chart_col.add_series({
    'name': 'Bug Analysis',
    'categories': '=Sheet1!$A$1:$D$1',
    'values': '=Sheet1!$A$2:$D$2',
    'points': [
        {'fill': {'color': '#00CD00'}},
        {'fill': {'color': 'red'}},
        {'fill': {'color': 'yellow'}},
        {'fill': {'color': 'gray'}},
    ],

})

# 设置图表的title 和 x，y轴信息
chart_col.set_title({'name': 'Bug Analysis'})

# 设置图表的风格
chart_col.set_style(10)

# 把图表插入到worksheet以及偏移
worksheet.insert_chart('B10', chart_col, {'x_offset': 25, 'y_offset': 10})
workbook.close()