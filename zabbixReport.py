'''
 * @Author: zhanxc 
 * @Date: 2020-12-31 17:51:18 
 * @Last Modified by:   zhanxc 
 * @Last Modified time: 2020-12-31 17:51:18 
'''
'''
自动获取zabbix当天巡检信息，可用于每天的巡检报告的数据来源
'''

import urllib
import json
import requests
import csv
import datetime
import time
import codecs
import logging
import Logger
# ZABBIX API
# 将实际的zabbix服务器IP替换成zabbixip
url = 'http://zabbixip:8080/zabbix/api_jsonrpc.php'
headers = {"Content-Type": "application/json-rpc"}
user = 'admin'
passwd = 'dbadmin'
auth = 1
# 巡检服务器IP列表
report_hostlist = ['127.0.0.1']
# 巡检服务器主机id列表
report_hostids = ['12120']
# 监控key
report_items = ['system.cpu.util[,,]','vm.memory.size[total]','vm.memory.size[available]','vfs.fs.size[/,used]','vfs.fs.size[/home,used]']
# 定义报告表头
csvheader = ['服务器IP地址','CPU使用率平均值', 'CPU使用率最大值', '总CPU核数','已使用内存平均值',
             '已使用内存最大值', '总内存大小','根目录磁盘空间平均值', '家目录磁盘空间平均值','巡检时间']
# 时间戳
x = (datetime.datetime.now()-datetime.timedelta(minutes=180)
     ).strftime("%Y-%m-%d %H:%M:%S")
y = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

def gettoken():
    data = {"jsonrpc": "2.0", "method": "user.login", "params": {
        "user": user, "password": passwd}, "id": 1, "auth": None}
    auth = requests.post(url=url, headers=headers, json=data)
    return json.loads(auth.content)['result']

def timestamps(x, y):
    p = time.strptime(x, "%Y-%m-%d %H:%M:%S")
    starttime = str(int(time.mktime(p)))
    q = time.strptime(y, "%Y-%m-%d %H:%M:%S")
    endtime = str(int(time.mktime(q)))
    return starttime, endtime

def login():
    
    data = {"jsonrpc": "2.0", "method": "user.login", "params": {
        "user": user, "password": passwd}, "id": 1, "auth": None}
    
    data = bytes(urllib.parse.urlencode(data), encoding='utf-8')
    ret = urllib.request.Request(url, headers=headers, data=data)
    res = urllib.request.urlopen(ret)
    aa = res.read().decode('utf-8')
    print(aa)

def logout(auth):
    data = {"jsonrpc": "2.0", "method": "user.logout",
            "params": [], "id": 1, "auth": auth}
    auth = requests.post(url=url, headers=headers, json=data)
    return json.loads(auth.content)

# 根据主机列表，遍历主机遍历、各个监控项
def get_report_data(report_hostids, report_items, token, timestamp,logger):
    row_records = []
    t_stamp = int(timestamp[0])
    t_local = time.localtime(t_stamp)
    report_time = time.strftime("%Y-%m-%d %H:%M:%S", t_local)
    # 巡检开始时间
    stime = time.time()
    log.info('巡检时间是 %s' % report_time)
    log.info('开始遍历主机列表')
    log.info('---------------')
    for host in report_hostids:
        # print(host)
        log.info('当前的主机id是 %s 监控项total是 %d' % (host,len(report_items)))
        item2 = []
        itemValueSet = {}

        # 主机巡检开始时间
        sstime = time.time()

        # 获取趋势数据
        for itemid in report_items:
            # 根据监控项获取监控id
            data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": ["itemid"],
                    "search": {
                        "key_": itemid
                    },
                    "hostids": host
                },
                "auth": token,
                "id": 1
            }
            getitem = requests.post(url=url, headers=headers, json=data)
            itemvalue = json.loads(getitem.content)['result']
            # 获取趋势数据
            trenddata = {
                "jsonrpc": "2.0",
                "method": "trend.get",
                "params": {
                    "output": ["itemid", "value_max", "value_avg",'value_min'],
                    "time_from": timestamp[0],
                    "time_till": timestamp[1],
                    "itemids": '%s' %(itemvalue[0]['itemid']),
                    "limit": 1
                },
                "auth": token,
                "id": 1
            }
            gettrend = requests.post(url=url, headers=headers, json=trenddata)
            trend = json.loads(gettrend.content)['result']
            item2.append(trend)

        # 赋值前判断返回值是否正确
        if len(item2[0]) != 0 :
            itemValueSet['CPU使用率最大值'] = round(float(item2[0][0]['value_max']), 2)
            itemValueSet['CPU使用率平均值'] = round(float(item2[0][0]['value_avg']), 2)
        else:
            itemValueSet['CPU使用率平均值'] = None
            itemValueSet['CPU使用率最大值'] = None
        if len(item2[1]) != 0 and len(item2[2]) != 0:
            vm_max = round(float(item2[1][0]['value_avg'])/1024/1024/1024 - float(item2[2][0]['value_min'])/1024/1024/1024, 2)
            vm_avg = round(float(item2[1][0]['value_avg'])/1024/1024/1024 - float(item2[2][0]['value_avg'])/1024/1024/1024, 2)
        else:
            vm_max = None
            vm_avg = None
        itemValueSet['已使用内存最大值'] = vm_max
        itemValueSet['已使用内存平均值'] = vm_avg
        if len(item2[1]) != 0:
            itemValueSet['总内存大小'] = round(float(item2[1][0]['value_avg'])/1024/1024/1024)
        if len(item2[3]) != 0:
            itemValueSet['根目录磁盘空间平均值'] = round(float(item2[3][0]['value_avg'])/1024/1024/1024, 2)
        else:
            itemValueSet['根目录磁盘空间平均值'] = None
        if len(item2[4]) != 0:
            itemValueSet['家目录磁盘空间平均值'] = round(float(item2[4][0]['value_avg'])/1024/1024/1024, 2)
        else:
            itemValueSet['家目录磁盘空间平均值'] = None
        
        log.info('id为%s 的主机巡检结束,耗时(s) %.2f' % (host,time.time()-sstime))

        itemValueSet['巡检时间'] = report_time
        
        row_records.append(itemValueSet)
    log.info('---------------')
    log.info('主机遍历结束:)，总耗时(s) %.2f' % (time.time()-stime))
    return row_records

def writecsv(gethist):
    # 生成巡检报告
    with open('data.csv', 'w', encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f, csvheader)
        writer.writeheader()
        for rows in gethist:
            writer.writerow(rows)

def get_day(day):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=day)
    yesterday = today - oneday
    yesterdaytime = yesterday.strftime('%Y%m%d')
    return yesterdaytime

# 日志设定
logdir = r'D:\workspace\autoreport_python\logs'
logfile = 'log' + str(get_day(0)) + '.txt'
log = Logger.get_logger(logdir,logfile)

log.info('---服务器巡检开始---')
# 正式函数调用
token = gettoken()
log.info('获取zabbix api访问权限')
timestamp = timestamps(x, y)
log.info('根据巡检列表进行巡检，开始进入巡检')
gethist = get_report_data(report_hostids, report_items, token, timestamp,logger=log)
log.info('准备写入文件')
writecsv(gethist)
log.info('写入完成')
logout(token)
log.info('---服务器巡检结束---')
