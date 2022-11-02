#coding:utf-8
import json
import requests

#中枢访问地址
url = 'https://pre.citybrain.org/api/getData'
dpAddress = '150849B971421009'

#解析从中枢返回的结果
def parse_data(content):
    content = json.loads(content)
    if len(content) < 2:
        return {"head": [], "value": []}
        
    return {
        "head": list(map(lambda x: x.strip(" "), content[0].split(";"))), # 表头
        "value": list(map(lambda x: x.strip(" ").split(";"), content[1:])) # 数据列表
    }

#访问中枢执行SQL，返回结果集
def fetch_data_from_ns(sql_cmd):

    reqBody = {
        "dpAddress": dpAddress,
        "payload": json.dumps({
            "selectSql": sql_cmd
        })
    }

    resp = requests.post(url=url, headers={"content-type": "application/json"}, json=reqBody)
    try:
        js = resp.json()
        if int(js["code"]) == 200:
            data = js["data"]
            return parse_data(data)
    except Exception as error:
        print(error) 
        
    return []
