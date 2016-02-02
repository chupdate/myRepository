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
        pageNos=7746
        self.cookie='JSESSIONID=pRF3WlWMx9mmjZRr5kjDB0zq4yRzbJR0BspkY3dl34WfM8rLZTNs!-1422204258; CNZZDATA1000300873=444788887-1453687937-http%253A%252F%252Fgsxt.saic.gov.cn%252F%7C1453687937'
        while True:
            try:
                pageNos+=1
                if pageNos>8253:break
                req=urllib.request.Request(
                   url='http://www.nmgs.gov.cn:7001/aiccips/main/abnInfoList.html',
                   data=self.getpagepostdata(pageNos),
                   headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                            'Content-Length':'19',
                            'Cookie':self.cookie
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
                                Name=jsonre['entName'].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,entNo=jsonre['entNo'],regID=jsonre['regNO'],type=jsonre['entType'],dec=jsonre['decOrg'])
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,jsonre)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo',
            data=self.getinfopostdata(ent['entNo'],ent['type'],ent['dec']),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                    'Cookie':self.cookie})
        inforesult=self.gethtml(req)
        infolist=inforesult.findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='内蒙古'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,11,1),enddate=date.today()-timedelta(days=0),fmode='a')


