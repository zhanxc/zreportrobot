#list
#function print
def uidPrint(useridlist):
    for uid in useridlist:
        #打印uid信息
        print("useridlist",uid)
#定义一个用户id列表
userid=[1,2,3,4,5]
#定义一个用户名列表
username=("1","2","3")
#赋值以前
uidPrint(userid)

print("----------")

#赋值以后
userid[1]=100
uidPrint(userid)