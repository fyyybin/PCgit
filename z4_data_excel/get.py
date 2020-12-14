import json
import xlrd
import os

wb = xlrd.open_workbook('z4.xls', logfile=open(os.devnull, 'w'))#打开文件
sheet1 = wb.sheet_by_index(0)
p = []
rows = sheet1.nrows  # 获取行内容
cols = sheet1.ncols  # 获取列内容
for i in range(rows):
    p = sheet1.cell_value(i,1).split('、')

