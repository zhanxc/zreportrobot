import json
url=''
headers={}
auth=''
starttime=20200601
endtime=20200617
#
def getHistoryData(itemid):
    #request json
    headers = {"Content-Type": "application/json-rpc"}
    data = json.dumps(
        {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": ["clock","value"],
            "time_from": starttime,
            "time_till": endtime,
            "itemids": itemid,
            "history": 0
        },
        "auth":"",
        #需要事先获取
        "id":1
        #自己定义
    })
    