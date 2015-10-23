__author__ = 'Chen'
#coding=utf-8
#如果程序异常，手动更换cookie和token
#日期顺序混乱
import  urllib.request,urllib.parse

import re
from datetime import *
from YCParser import YCParser
import json

class GetYCParser(YCParser):

    def getpagepostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'page':'%d'% pageNos,
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,encrpripid):
        postdata=urllib.parse.urlencode({
            'encrpripid':encrpripid
        }).encode('utf-8')
        return postdata

    def setdate(self,date_json):
        if not date_json:return ""
        day=date_json['date']
        month=date_json['month']+1
        year=date_json['year']+1900
        return date(year,month,day)

    def getentlist(self,startdate,enddate):
        pageNos=0
        #X-CSRF-TOKEN
        self.token='113251da-9962-448f-93cb-21601f75d2cf'
        self.cookie='JSESSIONID=w7Jne7e6DHP5Ce3X5mXpUiUF.undefined; CNZZDATA1000300906=689205639-1438063354-http%253A%252F%252Fgsxt.saic.gov.cn%252F%7C1444379643; SECSESSIONID=fc57d306ce4847417f3f5d9fd32ce2a5; ROBOTCOOKIEID=1082e2e8028316f76c583601b0ff27cd36d9d826'
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://211.141.74.198:8081/aiccips/pub/jyyc',
                data=self.getpagepostdata(pageNos),
                headers={'X-CSRF-TOKEN':self.token,
                         'Cookie':self.cookie,
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Content-Length': '6',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Host': '211.141.74.198:8081',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                         'Referer':'http://211.141.74.198:8081/aiccips/pub/abnormalrecordindex',
                         'Accept-Encoding':"gzip, deflate",
                         'X-Requested-With':"XMLHttpRequest",
                         'Connection':"keep-alive",
                         'Pragma':"no-cache",
                         'Cache-Control':"no-cache"}
            )
            result=self.gethtml(req)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            jsonlist=json.loads(str(result))
            if not jsonlist:break
            br=0
            for jsonre in jsonlist:
                cdate=self.setdate(jsonre['abntime'])
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        entdict=dict(Name=jsonre['entname'],pri=jsonre['pripid'],reg=jsonre['regno'],type=jsonre['enttype'])
                        self.PrintInfo(entdict,self.f)
            if br==1:break

    def PrintInfo(self,ent,f):
        req=urllib.request.Request(
            url='http://211.141.74.198:8081/aiccips/pub/jyyc/'+ent.get('type'),
            data=self.getinfopostdata(ent.get('pri')),
            headers={'X-CSRF-TOKEN':self.token,
                     'Cookie':self.cookie,
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Length': '107',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'X-Requested-With':'XMLHttpRequest',
                    'Host': '211.141.74.198:8081',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'}
        )
        inforesult=str(self.gethtml(req))
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=json.loads(inforesult)
            l=len(infolist)
            for i in range(l):
                f.write(ent.get('Name').strip()+'|')
                f.write(ent.get('reg')+'|')
                f.write(str(i+1)+'|')
                f.write(infolist[i]['specause']+'|')
                f.write(str(self.setdate(infolist[i]['abntime']))+'|')
                f.write(infolist[i]['remexcpres']+'|')
                f.write(str(self.setdate(infolist[i]['remdate']))+'|')
                f.write(infolist[i]['decorg']+'|')
                f.write('\n')

if __name__=='__main__':
    location='吉林'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,7,24),enddate=date.today())
