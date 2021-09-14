import xlwings as xw
def xlwings_test():
    app = xw.App(visible=True, add_book=False)
    # 新建工作簿 (如果不接下一条代码的话，Excel只会一闪而过，卖个萌就走了）
    wb = app.books.add()
    wb = app.books.open('test.xls')
    wb.save('test.xls')
    wb.close()
    app.quit()
    # 练习的时候建议直接用下面这条
    # wb = xw.Book('test.xls')
    # 这样的话就不会频繁打开新的Excel

def xlwings_save():
    # app = xw.App(visible=True, add_book=False)
    # # 新建工作簿 (如果不接下一条代码的话，Excel只会一闪而过，卖个萌就走了）
    # wb = app.books.add()
    # wb = app.books.open('test.xls')
    # wb.save('test.xls')
    # wb.close()
    # app.quit()
    # # 练习的时候建议直接用下面这条
    # # wb = xw.Book('test.xls')
    # # 这样的话就不会频繁打开新的Excel
    # 打开Excel程序，默认设置：程序可见，只打开不新建工作薄，屏幕更新关闭
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False

    # 文件位置：filepath，打开test文档，然后保存，关闭，结束程序
    filepath = r'test.xls'
    wb = app.books.open(filepath)
    wb.save()
    wb.close()
    app.quit()

def xlwings_create():
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    wb.save('xlwings.xls')
    wb.close()
    app.quit()

def xlwings_add():
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()

    # wb就是新建的工作簿(workbook)，下面则对wb的sheet1的A1单元格赋值
    wb.sheets['sheet1'].range('A1').value = '人生苦短,我用python'
    wb.save('xlwings_add.xls')
    wb.close()
    app.quit()

def xlwings_update():
    app = xw.App(visible=True, add_book=False)
    wb = app.books.open('xlwings_add.xls')
    # wb就是新建的工作簿(workbook)，下面则对wb的sheet1的A1单元格赋值
    wb.sheets['sheet1'].range('A1').value = '!'
    wb.save()
    wb.close()
    app.quit()

if __name__ == '__main__':
    # xlwings_test()
    # xlwings_save()
    # xlwings_create()
    # xlwings_add()
    xlwings_update()