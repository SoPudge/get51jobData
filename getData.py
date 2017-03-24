# -*- coding: utf-8 -*- 
from urllib import request,parse
#抓取信息类
##实现抓取信息的类，其中含有一个定义抓取内容的方法
##生成URL-GET数据的方法
##提交信息的方法
##存储获取信息的方法
##打印获取信息的方法
class getJobData():
    def __init__(self):
        pass
    def getData(self):
        searchUrl = 'http://m.51job.com/search/joblist.php?'
        with request.urlopen(searchUrl) as f:
            print(f.status,f.reason)
getjob = getJobData()
getjob.getData()
if __name__ == '__main__':
    getjob.getData()
