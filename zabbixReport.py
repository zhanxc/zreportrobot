#测试zabbix api接口

# from urllib.request import urlopen, Request
import urllib
# import urllib.parse
import json
import requests
import csv
import datetime
import time
import codecs
#ZABBIX API
url = 'http://zabbix_servverip/api_jsonrpc.php'
headers = {"Content-Type": "application/json-rpc"}
user = '管理员'
passwd = '管理员密码'
# 定义报告表头
csvheader = []
# 时间戳
x = (datetime.datetime.now()-datetime.timedelta(minutes=120)).strftime("Y%-%m-%d %H:%M:%S")
y = (datetime.datetime.now()).strftime("Y%-%m-%d %H:%M:%S")
def gettoken():
    data = {"jsonrpc":"2.0","method":"user.login","params":{"user":user,"password":passwd},"id":1,"auth":None}
    auth = requests.post(url=url,headers=headers,json=data)
    return json.loads(auth.content)['result']

def timestamps(x,y):
    p = time.strptime(x,"Y%-%m-%d %H:%M:%S")
    starttime = str(int(time.mktime(p)))
    q = time.strptime(y,"Y%-%m-%d %H:%M:%S")
    endtime = str(int(time.mktime(q)))
    return starttime,endtime

def login():
    # url='http://zabbix_servverip/api_jsonrpc.php'
    # headers={"Content-Type": "application/json-rpc"}
    # 字典转json
    data = '{"jsonrpc":"2.0","method":"user.login","params":{"user":user,"password":passwd},"id":1,"auth":null}'
    # print(data)
    #请求参数
    data = json.loads(data)
    print(data)
    data = bytes(urllib.parse.urlencode(data),encoding='utf-8')
    ret = urllib.request.Request(url, headers=headers,data=data)
    res = urllib.request.urlopen(ret)
    aa = res.read().decode('utf-8')
    print(aa)

def logout(auth):
    data = {"jsonrpc":"2.0","method":"user.logout","params":[],"id":1,"auth":auth}
    auth = requests.post(url=url,headers=headers,json=data)
    return json.loads(auth.content)

def gethosts(groupids,auth):
    data = {
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
            "output": ["name"],
            "groupids": groupids,
            "filter": {
                "status": "0"
            },
            "selectInterface": [
                "ip"
            ]
        },
        "auth": auth,
        "id": 1
    }
    gethost = requests.post(url=url,headers=headers,json=data)
    return json.loads(gethost.content)['result']

def gethist(gethosts,token,timestamp):
    row_records = []

    for host in gethosts:

        print(host)
        item1 = []
        item2 = []
        dic = {}

        for itemid in ['vfs.fs.size[total]','vm.memory.size[total]','system.cup.load']:
            # 根据监控项获取监控id
            data = {
                "jsonrpc":"2.0",
                "method":"item.get",
                "params":{
                "output": ["itemid"],
                "search": {
                    "key_": itemid
                },
                "hostids": host['hostid']
                },
                "auth": auth,
                "id": 1
            }
            getitem = requests.post(url=url,headers=headers,json=data)
            itemvalue = json.loads(getitem.content)['result']
            # 获取历史数据
            hisdata = {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                "output": "extend",
                "time_from": timestamp[0],
                # "time_till": timestamp[1],
                "hostids": 0,
                "sortfield": "clock",
                "sortorder": "DESC",
                "itemids": '%s' %(itemvalue[0]['itemid']),
                "limit": 1
                },
                "auth": auth,
                "id": 1
            }
            gethistory = requests.post(url=url,headers=headers,json=data)
            history = json.loads(gethistory.content)['result']
            item1 = item1.append(history)

            for itemid in ['vfs.fs.size[used]','vm.memory.size[used]','system.cup.load']:
            # 根据监控项获取监控id
            data = {
                "jsonrpc":"2.0",
                "method":"item.get",
                "params":{
                "output": ["itemid"],
                "search": {
                    "key_": itemid
                },
                "hostids": host['hostid']
                },
                "auth": auth,
                "id": 1
            }
            getitem = requests.post(url=url,headers=headers,json=data)
            itemvalue = json.loads(getitem.content)['result']
            # 获取趋势数据
            trendata = {
                "jsonrpc": "2.0",
                "method": "trend.get",
                "params": {
                "output": ["itemid", "value_max", "value_avg"],
                "time_from": timestamp[0],
                "time_till": timestamp[1],
                "itemids": '%s' %(itemvalue[0]['itemid']),
                "limit": 1
                },
                "auth": auth,
                "id": 1
            }
            gettrend = requests.post(url=url,headers=headers,json=data)
            trend = json.loads(gettrend.content)['result']
            item2 = item2.append(history)
        print(item1)
        print(item2)
        dic['Hostname'] = host['name']
        

def writecsv(gethist):
    pass

def getzabbixapiversion(url,headers,data):
    ret = urllib.request.Request(url, headers=headers,data=data)
    res = urllib.request.urlopen(ret)
    aa = res.read().decode('utf-8')
    print(aa)
    #
# getzabbixapiversion()
# login()
# 函数调用逻辑
# token = gettoken()
# timestamp = timestamps(x,y)
# gethosts = gethosts(groupids,token)
# gethist = gethist(gethosts,token,timestamp)
# writecsv(gethist)
# logout(token)