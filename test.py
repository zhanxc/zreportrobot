#测试
#FLASK测试
""" from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run()

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return '<h1>Welcome Home</h1>' """
#urllib测试
#不添加请求头部
""" from urllib import request

with request.urlopen('https://book.douban.com/subject/34986715/?icn=index-latestbook-subject') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', data.decode('utf-8')) """
#添加了请求头部
"""from urllib.request import urlopen, Request

url = 'https://book.douban.com/subject/34986715/?icn=index-latestbook-subject'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ret = Request(url, headers=headers)
res = urlopen(ret)
aa = res.read().decode('utf-8')
print(aa)"""
#
#读取JSON数据，然后解析为python对象
""" from urllib import request
from urllib.parse import urlparse

url='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json'
def fetchData(url):
    data = request.urlopen(url)
    #返回JSON数据
    print(data)
    parseData = urlparse(url)
    #解析URL数据，变成一个python对象（tuble）
    print(parseData)

#代码测试
fetchData(url) """
#list
#function print
def uidPrint(useridlist):
    for uid in useridlist:
        #打印uid信息
        print("useridlist",uid)
        #
    #
#python数据类型测试
#
#定义一个用户id有序列表
userid=[1,2,3,4,5]
#赋值以前
uidPrint(userid)
print("----------")
#赋值以后
userid[1]=100
uidPrint(userid)
userid.pop()
userid.append(99)
userid[2] = 22
#定义一个用户名不可变有序列表
username=("1","2","3")
uidPrint(username)
#username初始化后不可修改
#定义一个dict对象
dog={"name":"big yellow dog","sex":"female","age":19}
print(dog)
#定义一个set对象，提供list输入
passwd=([1,2,3,4])
print(passwd)
passwd.append(21)
passwd.remove(1)
#
