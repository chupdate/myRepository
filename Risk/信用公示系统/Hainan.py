__author__ = 'Chen'
#coding=utf-8
#有时可能无法读取经营异常数据
#（待清理）
import urllib.parse,urllib.request
import re
from datetime import *
from YCParser import YCParser
import time
import json

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'textfield':''
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,ent):
        postdata=urllib.parse.urlencode({
            'entNo':ent.get('entNo'),
            'entType':ent.get('entType')+'++',
            'regOrg':ent.get('regOrg')
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=-1
        while True:
            pageNos+=1
            time.sleep(1)
            req=urllib.request.Request(
                url='http://aic.hainan.gov.cn:1888/aiccips/main/abnInfoList.html',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                         'Accept':'application/json, text/javascript, */*; q=0.01',
                         'Content-Length':'19'}
            )
            result=str(self.gethtml(req))
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % (pageNos+1))
            resultlist=json.loads(result)['rows']
            br=0
            for result in resultlist:
                cdate=result['abnTimeStr']
                cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        entdict=dict(Name=result['entName'],reg=result['regNO'],entNo=result['entNo'],entType=result['entType'],regOrg=result['decOrg'])
                        self.PrintInfo(entdict,self.f)
            if br==1:break

    def PrintInfo(self,ent,f):
        time.sleep(2)
        req=urllib.request.Request(
            url='http://aic.hainan.gov.cn:1888/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo',
            data=self.getinfopostdata(ent),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                     'Content-Length':'71',
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'Cookie': 'JSESSIONID=CgsBFgdgVhxf2nCRj0NlnEeauZChK5_qoYwA.aiccips_1; CNZZDATA1000300888=150854017-1438154072-http%253A%252F%252Fgsxt.saic.gov.cn%252F%7C1444699325'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.findAll('td')
            l=int(len(infolist)/6)
            for j in range(l):
                f.write(ent.get('Name').replace('\n','').strip()+'|')
                f.write(ent.get('reg').strip()+'|')
                for k in range(6):
                    i=j*6+k
                    infostr=infolist[i].contents
                    if infostr:
                        infostr=infostr[0]
                        f.write(infostr.replace('\n','').strip())
                    f.write('|')
                f.write('\n')

if __name__=='__main__':
    location='海南'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,8,10),enddate=date.today()-timedelta(days=0))