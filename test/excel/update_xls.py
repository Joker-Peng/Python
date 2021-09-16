import xlrd
from xlutils.copy import copy

# import copy
def update_xls():
    workbook = xlrd.open_workbook('test.xls')  # 打开工作簿
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    sheet = workbook.sheet_by_index(0)
    col2 = sheet.col_values(1)  # 取出第二列
    cel_value = sheet.cell_value(1, 1)
    print(col2)
    print(cel_value)

    # 写入表格信息
    write_save = new_workbook.get_sheet(0)
    write_save.write(0, 0, "xlutils写入！")

    new_workbook.save("new_test.xls")  # 保存工作簿


if __name__ == '__main__':
    # read_xls("test.xls")
    update_xls()