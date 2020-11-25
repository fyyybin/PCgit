from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re
import collections
import json
"""
获取url的源html
"""
def scroll_page(url):
    browser = webdriver.Chrome('D:\Driver\chromedriver.exe')
    browser.get(url)
    html = browser.page_source
    return html
"""
提取网页全部内容
"""
def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all("div", class_="floatnone")
    #使用bs4提取全部的相关title和对应网站
    return content
"""
正则处理
"""
def re_data(content):
    dic = collections.OrderedDict()
    for i in content:
        Href = re.findall(r'href="([^"]+)"', i)
        Title = re.findall(r'title="([^"]+)"', i)
        #使用正则匹配相关的内容
        dic[Title[0]] = Href[0]
    return dic
"""
保存到json
"""
def savefile(dic):
    with open('dic_url_name.json', 'r') as s:
        old_dic = json.load(s)
    new_dic = dict(old_dic, **dic)
    with open('dic_url_name.json', 'w') as f:
        json_str = json.dumps(new_dic, indent=4, ensure_ascii=False)
        f.write(json_str)
def main():
    my_order_dict = collections.OrderedDict()
    #第一页的导入
    print('开始导入中药词典第1页-------------------------------------------------------')
    url = "http://www.a-hospital.com/w/%E4%B8%AD%E8%8D%AF%E5%9B%BE%E5%85%B8"
    html = scroll_page(url)
    content = get_data(html)
    con = str(content).strip('[').strip(']').split(',')
    my_order_dict = re_data(con)
    with open('dic_url_name.json', 'w') as f:
        json_str = json.dumps(my_order_dict, indent=4, ensure_ascii=False)
        f.write(json_str)
    sleep(3)
    print('第1页导入结束----------------------------------------------------------------')
    for i in range(2, 29):
        #1-9页，
        if i ==1 :
            k = ''
        else:
            k = '/' + str(i)
        print('开始导入中药词典第'+str(i)+'页-------------------------------------------------------')
        url = "http://www.a-hospital.com/w/%E4%B8%AD%E8%8D%AF%E5%9B%BE%E5%85%B8" + k
        html = scroll_page(url)
        content = get_data(html)
        con = str(content).strip('[').strip(']').split(',')
        my_order_dict = re_data(con)
        savefile(my_order_dict)
        sleep(3)
        print('第'+str(i)+'页导入结束----------------------------------------------------------------')
main()