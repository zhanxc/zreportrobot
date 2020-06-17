#list
#function print
def uidPrint(useridlist):
    for uid in useridlist:
        #打印uid信息
        print("useridlist",uid)
        #
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
#定义一个set对象，提供list输入
passwd=([1,2,3,4])
passwd.append(21)
passwd.remove(1)
