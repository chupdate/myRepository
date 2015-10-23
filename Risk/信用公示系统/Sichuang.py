__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse
import re
from datetime import *
import time
from YCParser import YCParser

class GetYCParser(YCParser):

    def getinfopostdata(self,pri):
        postdata=urllib.parse.urlencode({
            'method':'jyycInfo',
            'maent.pripid':pri,
            'czmk':'czmk6',
            'random':str(time.time()*1000)
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>7306:break
                url='http://gsxt.scaic.gov.cn/xxcx.do?method=ycmlIndex&random='+str(time.time()*1000)+\
                    '&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo='+str(pageNos)+'&yzm='
                result=self.gethtml(url,timeout=60)
                Namelist=result.findAll('li',attrs={'class':'tb-a1'})
                regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                del Namelist[0]
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
                                priName=Namelist[i].find('a')
                                Name=priName.contents[0]
                                reg=r'doOpen\(\'(.*?)\'\)'
                                pattern=re.compile(reg)
                                pri=pattern.findall(str(priName))[0]
                                regID=regIDlist[i].contents[0]
                                entdict=dict(Name=Name,regID=regID,Date=cdate,pri=pri)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://gsxt.scaic.gov.cn/ztxy.do',
            data=self.getinfopostdata(ent.get('pri')),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('tr',attrs={'name':'yc'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='四川'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,10),enddate=date.today()-timedelta(days=0))

