# -*- coding: UTF-8 -*-
import xlrd
import os
import json
import time
from pymongo import MongoClient
"""
check excel
"""
def inti():
    client = MongoClient(host='127.0.0.1', port=27017)
    db = client['emr']
    col = db['zju4h']
    data = col.find()
    with open('检验.json', 'r', encoding='utf-8') as f:
        q = json.load(f)
        f.close()
    A = list(q.keys())
    doc = []
    for x in data:
        document = {}
        document['入院记录'] = x['入院记录']
        document['首次病程记录'] = x['首次病程记录']
        if '出院记录' in x:
            document['出院记录'] = x['出院记录']
        for i in A:
            n = q.get(i).get("病历号")
            if x["首次病程记录"]["病历号"] == n:
                document["检验"] = q.get(i)
        doc.append(document)
    col.remove()
    for m in doc:
        col.insert_one(m)

    client.close()


def read_excel_1():
    print("开始提取浙四  检查  的excel脑梗数据--------------------------------")
    name = "检查" + ".xls"
    wb = xlrd.open_workbook(name, logfile=open(os.devnull, 'w'))  # 打开文件
    sheet1 = wb.sheet_by_index(0)  # 通过索引获取sheet2
    rows = sheet1.nrows  # 获取行内容
    cols = sheet1.ncols  # 获取列内容
    # 从第一行开始判断病历号
    p = []
    output = {}
    for i in range(1, rows):
        if sheet1.cell_value(i, 0) != sheet1.cell_value(i - 1, 0):
            p.append(i + 1)
    p.append(rows)
    for i in range(len(p) - 1):
        dic_small = {}
        number = int(sheet1.cell_value(p[i], 0))

        dic_big = {"病历号": str(number)}
        for j in range(p[i], p[i + 1] + 1):
            if sheet1.cell_value(j - 1, 1) != sheet1.cell_value(j - 2, 1) and j != p[i]:
                data_time = xlrd.xldate.xldate_as_datetime(sheet1.cell(j - 2, 4).value, 0)
                dic_small["日期"] = data_time.strftime("%Y-%m-%d %H:%M:%S")
                dic_big[sheet1.cell_value(j - 2, 1)] = dic_small
                dic_small = {}

            dic_small[sheet1.cell_value(j - 1, 2)] = sheet1.cell_value(j - 1, 3).replace('\n', '').replace(' ', '')
            if j == rows:
                dic_big[sheet1.cell_value(j - 2, 1)] = dic_small
        output[sheet1.cell_value(p[i], 0)] = dic_big
        with open('data1.json', 'w', encoding='utf-8') as f:
            json_str = json.dumps(output, indent=4, ensure_ascii=False)
            f.write(json_str)
    print("提取完成------------------------------------------")
"""
something excel
"""
def read_excel_2():
    print("开始提取浙四  检验  的excel脑梗数据--------------------------------")
    for x in [1,2,3]:
        print("start---------检验"+str(x)+"---------------------------------------------")
        name = "检验" + str(x) + ".xls"
        wb = xlrd.open_workbook(name, logfile=open(os.devnull, 'w'))#打开文件
        sheet_lsit = wb.sheet_names()
        for y in range(len(sheet_lsit)):
            print("          start-----------sheet"+str(y)+"------------------------------")
            sheet1 = wb.sheet_by_index(y)#通过索引获取sheet

            rows = sheet1.nrows  # 获取行内容
            cols = sheet1.ncols  # 获取列内容
            #从第一行开始判断病历号

            case = []
            output = {}
            # 将病历分类
            for i in range(1, rows):
                if sheet1.cell_value(i, 0) != sheet1.cell_value(i - 1, 0):
                    case.append(i + 1)
            case.append(rows)

            for i in range(len(case)-1):
                dic_small = {}
                dic_big = {}
                dic_ss = {}
                list = []
                number = int(sheet1.cell_value(case[i], 0))
                dic_count = {"病历号" : str(number)}
                a = 1
                for j in range(case[i], case[i+1]+1):

                    if sheet1.cell_value(j - 1, 3) != sheet1.cell_value(j - 2, 3) or sheet1.cell_value(j - 1, 2) != sheet1.cell_value(j - 2, 2):
                        if j != case[i]:
                            if sheet1.cell_value(j - 2, 3).replace('.', '_') in dic_small.keys():
                                data_time = xlrd.xldate.xldate_as_datetime(sheet1.cell(j - 2, 5).value, 0)
                                dic_small[sheet1.cell_value(j - 2, 3).replace('.', '_')][data_time.strftime("%Y-%m-%d %H:%M:%S")] = sheet1.cell_value(j - 2, 4)
                                if sheet1.cell_value(j - 1, 2) != sheet1.cell_value(j - 2, 2):
                                    dic_ss = {}
                            else:
                                dic_small[sheet1.cell_value(j - 2, 3).replace('.', '_')] = dic_ss
                                dic_ss = {}

                    if sheet1.cell_value(j - 1, 2) != sheet1.cell_value(j - 2, 2) and j != case[i]:
                        dic_big[sheet1.cell_value(j - 2, 2).replace('.', '_')] = dic_small
                        dic_small = {}

                    data_time = xlrd.xldate.xldate_as_datetime(sheet1.cell(j - 1, 5).value, 0)
                    dic_ss[data_time.strftime("%Y-%m-%d %H:%M:%S")] = sheet1.cell_value(j - 1, 4)

                    if j == rows:
                        dic_big[sheet1.cell_value(j - 2, 2).replace('.', '_')] = dic_small
                    if sheet1.cell_value(j - 1, 1) != sheet1.cell_value(j - 2, 1) and j != case[i]:
                        dic_count[sheet1.cell_value(j - 2, 1)] = dic_big
                        dic_big = {}
                        a += 1

                    if j == case[i + 1] and dic_big != {}:
                        dic_count[sheet1.cell_value(j - 2, 1)] = dic_big

                    output[sheet1.cell_value(case[i], 0)] = dic_count

            savefile(output, x, y)
            print("          保存成功！-----------------------------")
    print("提取完成------------------------------------------")
"""
保存到json
"""
def savefile(dic,name,sheet):
    with open('data'+str(name)+str(sheet)+'.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(dic, indent=4, ensure_ascii=False)
        f.write(json_str)

inti()