__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse

import re
from datetime import *
import json
from YCParser import YCParser

class GetYCParser(YCParser):

    def setdate(self,fdate):
        k1=fdate.find(' ')
        smonth=fdate[0:k1]
        table={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        month=table.get(smonth)
        k2=fdate.find(',')
        day=int(fdate[k1+1:k2])
        year=int(fdate[k2+2:k2+6])
        date0=date(year,month,day)
        return date0

    def getpagepostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'textfield':''
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,entNo,entType,regOrg):
        postdata=urllib.parse.urlencode({
            'entNo':entNo,
            'entType':entType,
            'regOrg':regOrg
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=-1
        while True:
            try:
                pageNos+=1
                if pageNos>8174:break
                req=urllib.request.Request(
                   url='http://www.nmgs.gov.cn:7001/aiccips/main/abnInfoList.html',
                   data=self.getpagepostdata(pageNos),
                   headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                            'Content-Length':'19',
                            'Cookie': 'CNZZDATA1000300873=998710141-1438070875-%7C1444465875; JSESSIONID=H9pBWYTKQ2K23pVZfhhCStMWZDVQM61w1z9l2WJTncTCsHYpgM2W!845010739; BIGipServerpool_10.10.10.2_7001=34212362.22811.0000'
                            })
                result=str(self.gethtml(req))
                result=json.loads(result)
                jsonlist=result['rows']
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % (pageNos+1))
                br=0
                for jsonre in jsonlist:
                    try:
                        cdate=self.setdate(jsonre['abnTime'])
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                entdict=dict(Name=jsonre['entName'],entNo=jsonre['entNo'],reg=jsonre['regNO'],type=jsonre['entType'],dec=jsonre['decOrg'])
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        print(ent)
        req=urllib.request.Request(
            url='http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo',
            data=self.getinfopostdata(ent['entNo'],ent['type'],ent['dec']),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                    'Cookie':'CNZZDATA1000300873=998710141-1438070875-|1444465875; JSESSIONID=c7JnWYjVvpnJJyJvMmvJdSV362hnsXLcD1nL9wbj851NQd4XWz0L!563693180; BIGipServerpool_10.10.10.2_7001=34212362.22811.0000'})
        inforesult=self.gethtml(req)
        infolist=inforesult.findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='内蒙古'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,10),enddate=date.today()-timedelta(days=0))


