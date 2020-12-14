import xlrd
import os
import json
import os
def combine_json():
    print("开始整合全部的json文件---------------------------------")
    os.rename('data10.json', 'data.json')
    for name in [1,2,3]:
        if name == 1:
            sheet = [1,2,3]
        if name == 2:
            sheet = [0,1,2,3,4,5,6,7,8,9]
        if name == 3:
            sheet = [0,1,2,3,4,5,6]
        for x in sheet:
            with open('data.json', 'r', encoding='utf-8') as f:
                p = json.load(f)
                f.close()
            with open('data'+str(name)+str(x)+'.json', 'r', encoding='utf-8') as f:
                q = json.load(f)
                f.close()
            A = list(p.keys())
            B = list(q.keys())
            print('开始整合---data'+str(name)+str(x)+'.json---------------------------------')
            for i in A:
                for j in B:
                    if i == j:
                        a = list(p.get(i).keys())
                        b = list(q.get(j).keys())
                        for m in a:
                            if m in b and m != "病历号":
                                new_dic = dict(p.get(i).get(m), **q.get(j).get(m))
                                p[i][m].update(new_dic)
                                del q[i][m]

                        new_dic = dict(p.get(i), **q.get(i))
                        p[i].update(new_dic)
                        del q[i]

            new_dic = dict(p, **q)
            with open('data.json', 'w', encoding='utf-8') as f:
                json_str = json.dumps(new_dic, indent=4, ensure_ascii=False)
                f.write(json_str)
            print('整合结束!--------------------------------------------')
            os.remove('data'+str(name)+str(x)+'.json')
    print('整合完成!--------------------------------------------------')

"""
检查.josn的title更改
"""
def change_title_test():
    print('开始改变检验相应的title---------------------')
    with open('data.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
        f.close()
    A = list(p.keys())
    for i in A:
        a = list(p.get(i).keys())
        for j in range(1, len(a)):
            new_dic = p[i][a[j]]
            del p[i][a[j]]
            p.get(i)["第"+str(j)+"次"] = new_dic
    with open('检验.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(p, indent=4, ensure_ascii=False)
        f.write(json_str)
    os.remove('data.json')
    print('改变完成!-----------------------------------')


"""
检验.json，将series转换为第几次访院
"""
def change_title_check():
    print("开始改变检查相应的title---------------------")
    with open('data1.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
        f.close()
    A = list(p.keys())

    for i in A:
        a = list(p.get(i).keys())
        for j in range(1, len(a)):
            new_dic = p[i][a[j]]
            del p[i][a[j]]
            p.get(i)["第" + str(j) + "次"] = new_dic

    with open('检查.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(p, indent=4, ensure_ascii=False)
        f.write(json_str)
    os.remove('data1.json')
    print('改变完成!-----------------------------------')

def number_get():
    with open('X.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
        f.close()
    with open('检验.json', 'r', encoding='utf-8') as f:
        q = json.load(f)
        f.close()
    A = list(q.keys())
    a = 0
    for i in A:
        n = q.get(i).get("病历号")
        for j in p:
            number = j.get("首次病程记录").get("病历号")
            if n == number:
                j["检验"] = q.get(i)
                a+=1
                print(number, a)

    with open('X.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(p, indent=4, ensure_ascii=False)
        f.write(json_str)



#combine_json()
change_title_check()