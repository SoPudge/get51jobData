# -*- coding: utf-8 -*- 
from urllib import request,parse
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import re
#抓取信息类
##实现抓取信息的类，其中含有一个定义抓取内容的方法
##生成URL-GET数据的方法
##提交信息的方法
##存储获取信息的方法
##打印获取信息的方法
class getCorpData(object):
    """docstring for getCorpData"""
    """抓取51job所有公司，并存储进入数据库"""
    """本类专门抓取公司详情信息，通过urllib.request抓取详情页，通过BS4来解析页面获取内容，返回字典"""
    def __init__(self):
        self.corpDetails = {}
    def getCorpDetails(self):
        #整个getCorpDetails方法，获取公司详情页面，并返回一个request对象
        #proxy_support = request.ProxyHandler({'http':'10.166.1.37:8080'})
        #opener = request.build_opener(proxy_support)
        #request.install_opener(opener)
        #header
        corpSearchUrl = request.Request('http://m.51job.com/search/codetail.php?')
        corpSearchUrl.add_header('Host','m.51job.com')
        corpSearchUrl.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0.1 Waterfox/51.0.1')
        corpSearchUrl.add_header('Accept','application/json')
        corpSearchUrl.add_header('Accept-Language','en-US,en;q=0.5')
        corpSearchUrl.add_header('X-Requested-With','XMLHttpRequest')
        corpSearchUrl.add_header('Referer','http://m.51job.com/search/joblist.php?keyword=python&keywordtype=2&jobarea=180200&landmark=&issuedate=&saltype=&degree=04&funtype=&indtype=&jobterm=&cotype=&workyear=02%2C03&cosize=&lonlat=&tubename=&tubeline=&radius=')
        corpSearchUrl.add_header('Cookie','guid=14742464778583340011; guide=1; ps=us%3DADpWOgJ%252BVmFSO18tUjEANwAtV2QHM1c0VixdPgg2BjEONFQ7AWtRYlM0CmYKaAAzUGADMFUvUGNQZ1B3AXMBeA%253D%253D%26%7C%26nv_3%3D; 51job=cuid%3D19936760%26%7C%26to%3DDTQCYFc8BDFRNgFqB2RXZAxzC2tVMVdhXD4AZFxgVWNcFAZsUDBWZlMsDDMBOwRqDHMLOwc0Wj9QYwFrDTFSaw0wAmlXNQ%253D%253D%26%7C%26cusername%3Dabcd666%2540126.com%26%7C%26cpassword%3D%26%7C%26ccry%3D.0V53QttMFPTE%26%7C%26cresumeid%3D19936760%26%7C%26cresumeids%3D.0V53QttMFPTE%257C.0Jjt9ZN%252F4DG2%257C.0gHlk7GWsUqg%257C%26%7C%26cname%3D%25D5%25C5%25D6%25D9%25E6%25EB%26%7C%26cemail%3Dabcd666%2540126.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26cenglish%3D0%26%7C%26cautologin%3D1%26%7C%26sex%3D0%26%7C%26cconfirmkey%3DabOtT9Sji8bbY%26%7C%26cnamekey%3Dab8fc7wVfJkzY; msearch=keyword%3Dpython%26%7C%26funtype%3D2400%26%7C%26jobarea%3D180200%26%7C%26navurl%3DL3NlYXJjaC9qb2JsaXN0LnBocD9rZXl3b3JkPXB5dGhvbiZrZXl3b3JkdHlwZT0yJmpvYmFyZWE9MTgwMjAwJmxhbmRtYXJrPSZpc3N1ZWRhdGU9JnNhbHR5cGU9JmRlZ3JlZT0wNCZmdW50eXBlPSZpbmR0eXBlPSZqb2J0ZXJtPSZjb3R5cGU9Jndvcmt5ZWFyPTAyJTJDMDMmY29zaXplPSZsb25sYXQ9JnR1YmVuYW1lPSZ0dWJlbGluZT0mcmFkaXVzPQ%3D%3D; usign=WmAHawV5Cj1UPVooC2ZUZFF8UGBSZ1I%2FViwGZQg2Bj8LMwFpAGRTYgZgCGACZ1diV2cKOFYsVGwBdVFPC3tVGA%3D%3D; partner=51jobhtml5')
        corpSearchUrl.add_header('DNT','1')
        corpSearchUrl.add_header('Connection','keep-alive')
        corpSearchUrl.add_header('Content-Length','0')
        #heaser-end
        
        #pararms
        corpPararmData = parse.urlencode({'coid':3598778})
        #url传输参数，因为以get方式传输，所以需要构建一个字典存储字符串
        corpGetDataUrl = "http://m.51job.com/search/codetail.php?%s" % corpPararmData
        #pararms-end
        with request.urlopen(corpGetDataUrl) as f:
            print(f.status,f.reason)
            #for k,v in f.getheaders():
            #    print('%s:%s' % (k,v))
            return f.read().decode('utf-8')

    def decodeCorpDetails(self,data):
        #整个方法传入一个需要解析的网页对象，通过bs来解析，获取公司详细信息
        soupCorpDetails = BeautifulSoup(data,'html.parser')
        corpName = soupCorpDetails.h1.get_text()
        #获取公司名称
        corpType = soupCorpDetails.find_all('font')[4].string
        corpEmplopyeeNum = soupCorpDetails.find_all('font')[5].string
        corpBusiness = soupCorpDetails.find_all('font')[6].string
        corpAddr = soupCorpDetails.select('.area')[0].string
        #公司性质，规模，行业获取
        self.corpDetails[corpName] = {'性质':corpType,'规模':corpEmplopyeeNum,'行业':corpBusiness,'地址':corpAddr}
        #存储到二维字典，以公司名为key，公司的性质，规模，行业为value
        return self.corpDetails

class getJobData(object):
    def __init__(self):
        pass
    def getData(self):
        #设置URLHEADERS
        searchUrl = request.Request('http://m.51job.com/search/joblist.php?')
        searchUrl.add_header('Host','m.51job.com')
        searchUrl.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0.1 Waterfox/51.0.1')
        searchUrl.add_header('Accept','application/json')
        searchUrl.add_header('Accept-Language','en-US,en;q=0.5')
        searchUrl.add_header('X-Requested-With','XMLHttpRequest')
        searchUrl.add_header('Referer','http://m.51job.com/search/joblist.php?keyword=python&keywordtype=2&jobarea=180200&landmark=&issuedate=&saltype=&degree=04&funtype=&indtype=&jobterm=&cotype=&workyear=02%2C03&cosize=&lonlat=&tubename=&tubeline=&radius=')
        searchUrl.add_header('Cookie','guid=14742464778583340011; guide=1; ps=us%3DADpWOgJ%252BVmFSO18tUjEANwAtV2QHM1c0VixdPgg2BjEONFQ7AWtRYlM0CmYKaAAzUGADMFUvUGNQZ1B3AXMBeA%253D%253D%26%7C%26nv_3%3D; 51job=cuid%3D19936760%26%7C%26to%3DDTQCYFc8BDFRNgFqB2RXZAxzC2tVMVdhXD4AZFxgVWNcFAZsUDBWZlMsDDMBOwRqDHMLOwc0Wj9QYwFrDTFSaw0wAmlXNQ%253D%253D%26%7C%26cusername%3Dabcd666%2540126.com%26%7C%26cpassword%3D%26%7C%26ccry%3D.0V53QttMFPTE%26%7C%26cresumeid%3D19936760%26%7C%26cresumeids%3D.0V53QttMFPTE%257C.0Jjt9ZN%252F4DG2%257C.0gHlk7GWsUqg%257C%26%7C%26cname%3D%25D5%25C5%25D6%25D9%25E6%25EB%26%7C%26cemail%3Dabcd666%2540126.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26cenglish%3D0%26%7C%26cautologin%3D1%26%7C%26sex%3D0%26%7C%26cconfirmkey%3DabOtT9Sji8bbY%26%7C%26cnamekey%3Dab8fc7wVfJkzY; msearch=keyword%3Dpython%26%7C%26funtype%3D2400%26%7C%26jobarea%3D180200%26%7C%26navurl%3DL3NlYXJjaC9qb2JsaXN0LnBocD9rZXl3b3JkPXB5dGhvbiZrZXl3b3JkdHlwZT0yJmpvYmFyZWE9MTgwMjAwJmxhbmRtYXJrPSZpc3N1ZWRhdGU9JnNhbHR5cGU9JmRlZ3JlZT0wNCZmdW50eXBlPSZpbmR0eXBlPSZqb2J0ZXJtPSZjb3R5cGU9Jndvcmt5ZWFyPTAyJTJDMDMmY29zaXplPSZsb25sYXQ9JnR1YmVuYW1lPSZ0dWJlbGluZT0mcmFkaXVzPQ%3D%3D; usign=WmAHawV5Cj1UPVooC2ZUZFF8UGBSZ1I%2FViwGZQg2Bj8LMwFpAGRTYgZgCGACZ1diV2cKOFYsVGwBdVFPC3tVGA%3D%3D; partner=51jobhtml5')
        searchUrl.add_header('DNT','1')
        searchUrl.add_header('Connection','keep-alive')
        searchUrl.add_header('Content-Length','0')
        #设置URLHEADERS结束

        #设置URL参数
        #urlParams = parse.urlencode()
        #设置URL参数结束
        with request.urlopen(searchUrl) as f:
            print(f.status,f.reason)
            for k,v in f.getheaders():
                print('%s:%s' % (k,v))
            print(f.read().decode('utf-8'))

    #def handleData(self):
    #    pass

#getjob = getJobData()
#getjob.getData()
getcorp = getCorpData()
corpdetails = getcorp.getCorpDetails()
result = getcorp.decodeCorpDetails(corpdetails)
print(result)
if __name__ == '__main__':
    #getcorp = getCorpData()
    getcorp = getCorpData()
    corpdetails = getcorp.getCorpDetails()
    result = getcorp.decodeCorpDetails(corpdetails)
    print(result)
