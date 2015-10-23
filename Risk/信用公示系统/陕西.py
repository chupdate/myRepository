__author__ = 'Chen'
#coding=utf-8
#日期顺序有问题
import urllib.parse,urllib.request
import re
from datetime import *
from YCParser import YCParser
import time

class GetYCParser(YCParser):

    def getinfopostdata(self,ent):
        postdata=urllib.parse.urlencode({
            'method':'jyycInfo',
            'maent.pripid':ent.get('pri'),
            'czmk':'czmk6',
            'random':time.time()
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                req=urllib.request.Request(
                    url='http://117.22.252.219:8002/xxcx.do?method=ycmlIndex&random='+str(time.time()*1000)+'&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo='+str(pageNos)+'&yzm=',
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req,timeout=60)
                infolist=result.findAll('a',attrs={'onclick':re.compile(r'javascript:doOpen*')})
                regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                del regIDlist[0]
                del datelist[0]
                l=len(datelist)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        cdate=str(datelist[i].contents[0])
                        reg=r'年(.*?)月'
                        pattern=re.compile(reg)
                        month=int(pattern.findall(cdate)[0])
                        reg=r'月(.*?)日'
                        pattern=re.compile(reg)
                        day=int(pattern.findall(cdate)[0])
                        cdate=date(int(cdate[0:4]),month,day)
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=infolist[i].contents[0]
                                regID=regIDlist[i].contents[0]
                                pri=self.dealID(infolist[i].get('onclick'))
                                entdict=dict(Name=Name,regID=regID,Date=cdate,pri=pri)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://117.22.252.219:8002/ztxy.do',
            data=self.getinfopostdata(ent),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table',attrs={'id':'table_yc'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='陕西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,7,1),enddate=date.today()-timedelta(days=1))