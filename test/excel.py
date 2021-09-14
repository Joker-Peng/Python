import xlrd
import xlwt

def read_xls(filename):
    xlsx = xlrd.open_workbook(filename)
    # 通过sheet名查找：xlsx.sheet_by_name("sheet1")
    # 通过索引查找：xlsx.sheet_by_index(3)
    table = xlsx.sheet_by_index(0)

    # 获取单个表格值 (2,1)表示获取第3行第2列单元格的值
    value = table.cell_value(2, 1)
    print("第3行2列值为", value)

    # 获取表格行数
    nrows = table.nrows
    print("表格一共有", nrows, "行")

    # 获取表格行数
    ncols = table.ncols
    print("表格一共有", ncols, "列")

    # 获取最后一列所有值（列表生成式）
    name_list = [str(table.cell_value(i, ncols-1)) for i in range(0, nrows)]
    print("最后一列所有的值：", name_list)

    # 获取最后一列所有值数据类型（列表生成式）
    type_list = [table.cell_type(i, ncols-1) for i in range(0, nrows)]
    print("最后一列所有的值数据类型：", type_list)

def write_xls():
    # 创建新的workbook（其实就是创建新的excel）
    workbook = xlwt.Workbook(encoding='ascii')

    # 创建新的sheet表
    worksheet1 = workbook.add_sheet("My new Sheet1")

    # 初始化样式
    style = xlwt.XFStyle()
    # 为样式创建字体
    font = xlwt.Font()
    font.name = '宋体'  # 字体
    font.bold = True  # 加粗
    font.underline = True  # 下划线
    font.italic = True  # 斜体

    # 设置边框样式
    borders = xlwt.Borders()  # Create Borders

    # May be:   NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR,
    #           MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED,
    #           MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    # DASHED虚线
    # NO_LINE没有
    # THIN实线

    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40

    # 设置背景色
    pattern = xlwt.Pattern()

    # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN

    # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow,
    # 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow ,
    # almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    pattern.pattern_fore_colour = 5

    # 设置单元格对齐
    al = xlwt.Alignment()
    # VERT_TOP = 0x00       上端对齐
    # VERT_CENTER = 0x01    居中对齐（垂直方向上）
    # VERT_BOTTOM = 0x02    低端对齐
    # HORZ_LEFT = 0x01      左端对齐
    # HORZ_CENTER = 0x02    居中对齐（水平方向上）
    # HORZ_RIGHT = 0x03     右端对齐
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al

    # 设置样式
    style.font = font
    style.borders = borders  # Add Borders to Style
    style.pattern = pattern

    # 设置列宽
    worksheet1.col(0).width = 256 * 40

    # 往表格写入内容
    worksheet1.write(0, 0, "内容1",style)
    worksheet1.write(2, 1, "内容2")


    # 设置行高
    style = xlwt.easyxf('font:height 360;')  # 18pt,类型小初的字号
    row = worksheet1.row(0)
    row.set_style(style)
    # todo: 注意对照sheet1 和 sheet2 A1之间的差异;

    # 合并单元格, 第二行到第二行的 第一列到第四列
    worksheet1.write_merge(1, 1, 0, 3, '合并单元格')

    # 创建新的sheet表
    worksheet2 = workbook.add_sheet("My new Sheet2")

    # 往表格写入内容
    worksheet2.write(0, 0, "内容3",style)
    worksheet2.write(0, 1, "内容4")
    worksheet2.col(0).width = 256 * 40

    # 保存
    workbook.save("test3.xls")

if __name__ == '__main__':
    # read_xls("test.xls")
    write_xls()