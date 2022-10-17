#coding:utf-8
import pandas as pd
import numpy as np
import json
from multiprocessing import Manager,Pool,Lock,Value
import requests
import time
import csv
import codecs
from tqdm import tqdm

#准备多进程输出共享变量
manager = Manager()
lock = Lock()
Counter = Value('i', 0)
data_list_total = manager.list([])

#并发度设置
cnt = 1

#中枢访问地址
url = "https://pre.citybrain.org/api/getData"

def parse_data(content):
    content = json.loads(content)
    if len(content) < 2:
        return {"head": [], "value": []}
        
    return {
        #"head": list(map(lambda x: x.strip(" "), content[0].split(";"))), # 表头
        "value": list(map(lambda x: x.strip(" ").split(";"), content[1:])) # 数据列表
    }

def search_info(start,dataframe):

    global data_list_total
    global lock
    global Counter

    data_list = []
    try:
        if dataframe[0].size > 1:
            lon1 = float(dataframe[0][start])
            lat1 = float(dataframe[1][start])
            lon2 = float(dataframe[2][start])
            lat2 = float(dataframe[3][start])
            npstr= str(dataframe[4][start])[2:-1]
            city = str(dataframe[5][start])[2:-1]
        else:
            lon1 = float(dataframe[0])
            lat1 = float(dataframe[1])
            lon2 = float(dataframe[2])
            lat2 = float(dataframe[3])
            npstr= str(dataframe[4])[2:-1]
            city = str(dataframe[5])[2:-1]  

        sql_cmd =  'select count(1) as edges,sum(distance) as distance ' + \
                   'from ( ' + \
                        'select lsid,sum(distance) as distance '  + \
                        'from( ' + \
                            'SELECT lsid,geo_distance(x1,y1,x2,y2) as distance  ' + \
                                'FROM ( ' + \
                                '  select lsid,osmid_start_x x1,osmid_start_y y1, osmid_end_x x2,osmid_end_y y2, pnpoly(osmid_start_x,osmid_start_y,\'' + npstr + '\') as nppoly  ' + \
                                '  from osm_split_edge_roadnet_t  ' + \
                                '  where osmid_start_x  < ' + str(lon2) + ' and osmid_start_x >  ' + str(lon1) + '  and osmid_start_y < ' + str(lat2) + '  and osmid_start_y > ' + str(lat1)  +  \
                                ' ) ' + \
                            'where  nppoly = true ' + \
                        ') ' + \
                        'group by lsid ' + \
                    ')'

        values = {"dpAddress":"150849B971421009",
            "payload": 
            "{\"selectSql\":\"" + sql_cmd + "\"}"}
        values_json = json.dumps(values)
        #print(sql_cmd)

        req = requests.post(url, headers={'content-type':'application/json'},data=values_json)
        js = req.json()
        data = js["data"]
        lst = parse_data(data)

        if len(data) > 2:
            item = lst.popitem()
            if int(item[1][0][0]) > 0:
                ls = [item[1][0][0],item[1][0][1],city]
                data_list.append(ls)
    except Exception as e1:
        ls = [0,0,city]
        data_list.append(ls)

    data_list_total.extend(data_list)

def data_write_csv_aggre(file_name, datas):
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    
    file_dict = dict()
    file_dict_cnt = dict()

    for i in range(datas.__len__()):
        data = datas.pop()

        city = data[2]
        city = city.replace(']','')
        result = file_dict.get(city)
        try:

            if result :
                result = ( (int(result[0]) + int(data[0])),(float(result[1]) + float(data[1])) )
                file_dict_cnt[city] = file_dict_cnt.get(city) + 1
            else:
                result = ( int(data[0]),float(data[1]))
                file_dict_cnt[city] = 1

            file_dict[city] = result

        except Exception as e1:
            print(e1)

    for key in file_dict.keys():
        #cnt = file_dict_cnt.get(city)
        data = (key, int(file_dict[key][0]),float(file_dict[key][1]) )
        writer.writerow(data)

#load polygon from csv
polygon = np.loadtxt('./polygon.csv',
        dtype={'names': ('x1', 'y1', 'x2','y2','npstr','city'),
        'formats': ('f4', 'f4', 'f4','f4','S400000','S40')},delimiter=';',,unpack=True)
total = polygon[0].size

#启动时间
time1 = time.time()
print("start...")

for j in tqdm(range(int(total/cnt)+1)):

    pool = Pool(cnt)
    try:
        for i in range(cnt):
            if( j*cnt + i >= total):
                break
            pool.apply_async(func=search_info,args=(j*cnt + i,polygon))

    finally:
        pool.close()
        pool.join()
        del pool

#输出该year/month的结果文件
file='./result.csv'
data_write_csv_aggre(file,data_list_total)

#pool.close()
del Counter
del lock
del data_list_total

#分析结束时间
time2 = time.time()
elasped = time2 - time1
print("总用时={:.2f} 秒".format(elasped))


