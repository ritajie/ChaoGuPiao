"""解析excel表 不管是读取还是写入"""
import xlwt
import xlrd
import time


def get_nameid():
    """return 字典 key=name value=id 类型str"""
    name_id = {}

    filepath1 = R"上交所A股代码.xlsx"
    filepath2 = R"深交所上市公司代码.xlsx"
#   filepath_xiaoyang = "小样.xlsx"
    file1 = xlrd.open_workbook(filepath1)
    sheet1 = file1.sheets()[0]
    rows1 = sheet1.nrows  # 行数
    file2 = xlrd.open_workbook(filepath2)
    sheet2 = file2.sheets()[0]
    rows2 = sheet2.nrows  # 行数

    for row in range(1, rows1):
        name = sheet1.cell(row, 0).value.strip()
        id = str(int(sheet1.cell(row, 1).value))
        name_id[name] = id

    for row in range(1, rows2):
        id = sheet2.cell(row, 0).value
        name = sheet2.cell(row, 1).value
        if len(name) < 2:  # 有空行
            continue
        ans[name] = id

    return name_id


def save_in_excel(ansdict, filepath=""):
    """保存结果到excel表中 默认路径是代码文件所在路径"""
    #新建表
    excel = xlwt.Workbook()
    sheet = excel.add_sheet(time.ctime().replace(" ", "_").replace(":", "_"))
    #写第一行
    sheet.write(0, 0, "名称")
    sheet.write(0, 1, "ID")
    sheet.write(0, 2, "成交量")
    sheet.write(0, 3, "振幅")
    sheet.write(0, 4, "换手")
    sheet.write(0, 5, "市盈率")
    #写正儿八经的数据
    hang = 1
    for name in ansdict:
        information_dict = ansdict[name]
        id = information_dict["ID"]
        chengjiaoliang = information_dict["成交量"]
        zhenfu = information_dict["振幅"]
        huanshou = information_dict["换手"]
        shiyinglv = information_dict["市盈率"]

        sheet.write(hang, 0, name)
        sheet.write(hang, 1, id)
        sheet.write(hang, 2, chengjiaoliang)
        sheet.write(hang, 3, zhenfu)
        sheet.write(hang, 4, huanshou)
        sheet.write(hang, 5, shiyinglv)

        hang += 1
    if filepath != "" and filepath[-1] != R"/":
        filepath += R"/"

    excel.save(R"%s股票爬取结果_%s.xls" % (filepath, time.ctime().replace(" ", "_").replace(":", "_")))
