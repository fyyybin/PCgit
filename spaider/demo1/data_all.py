from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox") # linux only
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver

def scroll_page(url):

    #browser = webdriver.Chrome('D:\Driver\chromedriver.exe')
    browser = getDriver()
    browser.get("http://www.a-hospital.com"+url)
    html = browser.page_source
    return html


"""
end标签
"""
def get_end(html):
    end_1 = []
    # end标签
    soup = BeautifulSoup(html, 'lxml')
    end = soup.find_all(class_="navbox")
    if end:
        end_t = str(end).strip('[').strip(']')
        end_1 = re.findall(r'[<](.*?)[>]', end_t)
        end_t = '<' + end_1[0] + '>'
        return end_t
    else:
        return False


"""
table标签,分类
"""
def get_table(html):
    con = []
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(class_="mw-headline")
    num = len(content)
    for i in range(num):
        con.append(str(content[i]))
    return con


"""
提取网页全部内容
"""
def get_data(html,con,end,name):

    table = get_title(html)  # list
    soup = BeautifulSoup(html, 'lxml')
    num = len(con)
    #图片png标签
    png = soup.find_all(class_="thumbcaption")
    png_name = re.sub('\<.*?\>', '', str(png)).replace('\n', '').replace(' ', '')


    #标签分块
    for i in range(num):
        if i != 0 and i != num-1:
            html = html.replace(con[i], '</div>' + con[i])
        if i != num-1:
            html = html.replace(con[i], con[i] + '<div id="' + str(i) + '">')
        if i == num-1:
            html = html.replace(end, '</div>' + end)


    soup = BeautifulSoup(html, 'lxml')
    dic = {}
    dic['中药名称'] = name

    if table == []:
        table.append("内容")

    for i in range(len(table)):
        title = soup.find_all('div', id=str(i))
        # 转换成string
        t = re.sub('\<.*?\>', '', str(title)).replace('\n', '').replace('\"', '"')

        if png_name in t:
            t = t.strip(png_name)

        dic[table[i]] = t
    return dic


"""
提取title
"""
def get_title(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find_all(class_="mw-headline")
    #转换成string
    title = re.sub('\<.*?\>', '', str(title))
    title = title.strip('[').strip(']').strip(' ').split(',')
    del title[-1]
    # 正则处理数据
    return title


"""
保存到json
"""
def savefile(dic):
    with open('./dic2.json', 'a',encoding="utf-8") as f:
        json_str = json.dumps(dic, indent=4, ensure_ascii=False)
        f.write(json_str)
        f.write(',')
    print('导入结束----------------------------------------------------------------')
def main():

    with open('dic_url_name.json', 'r') as s:
        item_dic = json.load(s)
    name = []
    for i in item_dic.keys(): 
        name.append(i)

    for i in range(194,200):
        print('开始导入中药词典第'+str(i)+'个-------------------------------------------------------'+str(name[i]))
        html = scroll_page(item_dic[name[i]])
        end = get_end(html)
        table = get_table(html)
        if end and table:
            dic = get_data(html,table,end,name[i])
            if i == 0:
                with open('./dic2.json', 'w',encoding="utf-8") as f:
                    json_str = json.dumps(dic, indent=4, ensure_ascii=False)
                    f.write(json_str)
                    f.write(',')
                print('导入结束----------------------------------------------------------------')
            else:
                savefile(dic)
        else:
            print('中药'+str(name[i])+'导入失败!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-')
main()