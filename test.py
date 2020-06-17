#list
#function print
def uidPrint(useridlist):
    for uid in useridlist:
    print("useridlist",uid)
#
userid=[1,2,3,4,5]
#
username=("1","2","3")
uidPrint(userid)
userid[1]=100
uidPrint(userid)