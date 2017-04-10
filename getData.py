# -*- coding: utf-8 -*- 
from urllib import request,parse
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import json
import re
import time
import sqlite3
#抓取信息类
##实现抓取信息的类，其中含有一个定义抓取内容的方法
##生成URL-GET数据的方法
##提交信息的方法
##存储获取信息的方法
##打印获取信息的方法
def headers():
    headers = {'Host':'m.51job.com', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0.1 Waterfox/51.0.1' , 'Accept':'application/json', 'Accept-Language':'en-US,en;q=0.5', 'X-Requested-With':'XMLHttpRequest', 'Referer':'http://m.51job.com/search/joblist.php?keyword=python&keywordtype=2&jobarea=180200&landmark=&issuedate=&saltype=&degree=04&funtype=&indtype=&jobterm=&cotype=&workyear=02%2C03&cosize=&lonlat=&tubename=&tubeline=&radius=', 'Cookie':'guid=14742464778583340011; guide=1; ps=us%3DADpWOgJ%252BVmFSO18tUjEANwAtV2QHM1c0VixdPgg2BjEONFQ7AWtRYlM0CmYKaAAzUGADMFUvUGNQZ1B3AXMBeA%253D%253D%26%7C%26nv_3%3D; 51job=cuid%3D19936760%26%7C%26to%3DDTQCYFc8BDFRNgFqB2RXZAxzC2tVMVdhXD4AZFxgVWNcFAZsUDBWZlMsDDMBOwRqDHMLOwc0Wj9QYwFrDTFSaw0wAmlXNQ%253D%253D%26%7C%26cusername%3Dabcd666%2540126.com%26%7C%26cpassword%3D%26%7C%26ccry%3D.0V53QttMFPTE%26%7C%26cresumeid%3D19936760%26%7C%26cresumeids%3D.0V53QttMFPTE%257C.0Jjt9ZN%252F4DG2%257C.0gHlk7GWsUqg%257C%26%7C%26cname%3D%25D5%25C5%25D6%25D9%25E6%25EB%26%7C%26cemail%3Dabcd666%2540126.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26cenglish%3D0%26%7C%26cautologin%3D1%26%7C%26sex%3D0%26%7C%26cconfirmkey%3DabOtT9Sji8bbY%26%7C%26cnamekey%3Dab8fc7wVfJkzY; msearch=keyword%3Dpython%26%7C%26funtype%3D2400%26%7C%26jobarea%3D180200%26%7C%26navurl%3DL3NlYXJjaC9qb2JsaXN0LnBocD9rZXl3b3JkPXB5dGhvbiZrZXl3b3JkdHlwZT0yJmpvYmFyZWE9MTgwMjAwJmxhbmRtYXJrPSZpc3N1ZWRhdGU9JnNhbHR5cGU9JmRlZ3JlZT0wNCZmdW50eXBlPSZpbmR0eXBlPSZqb2J0ZXJtPSZjb3R5cGU9Jndvcmt5ZWFyPTAyJTJDMDMmY29zaXplPSZsb25sYXQ9JnR1YmVuYW1lPSZ0dWJlbGluZT0mcmFkaXVzPQ%3D%3D; usign=WmAHawV5Cj1UPVooC2ZUZFF8UGBSZ1I%2FViwGZQg2Bj8LMwFpAGRTYgZgCGACZ1diV2cKOFYsVGwBdVFPC3tVGA%3D%3D; partner=51jobhtml5', 'DNT':'1', 'Connection':'keep-alive', 'Content-Length':'0'}
    return headers
def Parmas(pageno = 1):
    Parma = {'keyword':'it', 'keywordtype':'2', 'jobarea':'180000', #'landmark':, #'issuedate':, #'saltype':, #'degree':, #'funtype':, #'indtype':, #'jobterm':, #'cotype':, #'workyear':, #'cosize':, #'lonlat':, #'tubename':, #'tubeline':, #'radius':
            } 
    Parma['pageno'] = pageno
    urlParams = parse.urlencode(Parma)
    return urlParams

class getIDs(object):
    def __init__(self):
        #构建get url，先构建完成带参数url，在附加req
        getUrl = '%s%s' % ('http://m.51job.com/search/joblist.php?',Parmas())
        getreq = request.Request(getUrl,headers = headers()) 
        #get方法获取搜索数据
        with request.urlopen(getreq) as f:
            htmlresult = f.read().decode('utf-8')
        #匹配一共有多少个搜索结果
        partten = re.compile(r'(<p class="result">为您找到相关结果约<span>)(\d{0,9})(</span>个</p>)')
        self.searchresult = partten.search(htmlresult).group(2)

    def getdata(self,pageno=1):
        #先附加req，提交时post参数，参数必须ascii，前程无忧提交的是空数据，请求的网址是带参数的，因为返回json过大，GET无法支持
        postUrl = '%s%s' % ('http://m.51job.com/ajax/search/joblist.ajax.php?',Parmas(pageno))
        postreq = request.Request(postUrl,headers = headers())
        #post方法获取搜索结果并用json解析出来
        with request.urlopen(postreq) as f:
            jsonresult = f.read().decode('utf-8')
            dictresult = json.loads(jsonresult)
        return dictresult

    def decode(self,**kwargs):
        kwargs = kwargs
        jobco = []
        #输出整个页面job结果，每页30个
        for n in range(len(kwargs['data'])):
            jobid = kwargs['data'][n]['jobid']
            coid = kwargs['data'][n]['coid']
            jobco.append((jobid,coid))
        return jobco

class getCorpData(object):
    """docstring for getCorpData"""
    """抓取51job所有公司，并存储进入数据库"""
    """本类专门抓取公司详情信息，通过urllib.request抓取详情页，通过BS4来解析页面获取内容，返回字典"""
    def __init__(self):
        #header
        self._corpSearchUrl = 'http://m.51job.com/search/codetail.php?'
        self._corpSearchreq = request.Request(self._corpSearchUrl,headers = headers)
        #heaser-end
        self._corpDetails = {}

    def getCorpDetails(self):
        corpPararmData = parse.urlencode({'coid':3598778})
        corpGetDataUrl = '%s%s' % (self._corpSearchreq,corpPararmData)
        with request.urlopen(corpGetDataUrl) as f:
            print(f.status,f.reason)
            #for k,v in f.getheaders():
            #    print('%s:%s' % (k,v))
            return f.read().decode('utf-8')

    def decodeCorpDetails(self,data):
        soupCorpDetails = BeautifulSoup(data,'html.parser')
        corpName = soupCorpDetails.h1.get_text()
        #获取公司名称
        corpType = soupCorpDetails.find_all('font')[4].string
        corpEmplopyeeNum = soupCorpDetails.find_all('font')[5].string
        corpBusiness = soupCorpDetails.find_all('font')[6].string
        corpAddr = soupCorpDetails.select('.area')[0].string
        #公司性质，规模，行业获取
        self._corpDetails[corpName] = {'性质':corpType,'规模':corpEmplopyeeNum,'行业':corpBusiness,'地址':corpAddr}
        #存储到二维字典，以公司名为key，公司的性质，规模，行业为value
        return self._corpDetails

class storage(object):
    '''
    执行三个存储方法，分别存储jobid和coid，jobid明细，coid明细
    '''
    def __init__(self):
        self.conn = sqlite3.connect('job.db')
        self.__c = self.conn.cursor()
        self.__c.execute('CREATE TABLE IF NOT EXISTS ids (jobid TEXT PRIMARY KEY,coid TEXT)')

    def storIDs(self,*args):
        args = args
        self.__c.executemany('INSERT INTO ids VALUES (?,?)',args)


if __name__ == '__main__':
    templist = []
    n = 0#设置存储步进
    allid = getIDs()
    searchno = allid.searchresult
    allpage = '%d' % ((int(searchno) / 30) + 2)
    allpage = int(allpage)
    print(allpage)
    t1 = time.time()
    for i in range(1,allpage):
        n = n + 1#设置存储步进
        #设置抓第第几页
        everypage = allid.getdata(i)
        everyid = allid.decode(**everypage)
        print(everyid)
        templist.extend(everyid)
        print('完成第 %s/%s 页的抓取，并存入临时list当中' % (i,allpage-1))
        print('')
        store = storage()#初始化数据存储方法
        if n == 20:
            print('开始临时插入数据库')
            store.storIDs(*templist)
            store.conn.commit()
            templist = []#重置临时数据
            n = 1#重置步进
    print('插入最后一次数据库')
    store.storIDs(*templist)
    store.conn.commit()
    store.conn.close()
    t2 = time.time()
    t = (t2-t1) * 100
    print('插入完成，合计耗时 %s 秒' % t)
