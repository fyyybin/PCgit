import pymongo
import time,datetime
import xlrd
import os
def process1():
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client['emr']
    col_from = db['zju4h']
    documents = col_from.find()

    wb = xlrd.open_workbook('z4.xls', logfile=open(os.devnull, 'w'))  # 打开文件
    sheet_test = wb.sheet_by_index(1)
    rows = sheet_test.nrows  # 获取行内容
    cols = sheet_test.ncols  # 获取列内容
    List = []
    for row in range(rows):
        List1 = []
        List1.append(sheet_test.cell_value(row, 0))
        List1.append(sheet_test.cell_value(row, 1))
        List1.append(sheet_test.cell_value(row, 2))
        List.append(List1)

    for doc in documents:
        Data = {}
        old_date = doc['入院记录']['入院时间']
        if doc.get("检验"):
            jianyan_page = doc.get("检验")
            for LIST in List:
                Data.update(search_index(jianyan_page, LIST[0], LIST[1], LIST[2], old_date))

        print(Data)
"""
获取相应指标并赋值
"""
def search_index(page, Name, Range, _name, old_date):
    date = {}
    data = {}
    list_time = list(page.keys())
    for time in list_time:
        if time == '病历号':
            data['BLH'] = page.get(time)
        else:
            list_title = list(page.get(time).keys())
            for title in list_title:
                if title in Range and Name in list(
                        page.get(time).get(title).keys()):
                    date.update(page.get(time).get(title).get(Name))
    if date:
        index = deal_date(old_date, list(date.keys()))
        data[_name] = date[index]
    return data
"""
计算最近日期
"""
def deal_date(old_date, date):
    timeOld = int(time.mktime(time.strptime(old_date, "%Y-%m-%d %H:%M:%S")))

    select = abs(timeOld - int(time.mktime(time.strptime(date[0], "%Y-%m-%d %H:%M:%S"))))
    index = 0
    for i in range(1, len(date)):
        select2 = abs(timeOld - int(time.mktime(time.strptime(date[i], "%Y-%m-%d %H:%M:%S"))))
        if select > select2:
            select = select2
            index = i
    return date[index]

process1()