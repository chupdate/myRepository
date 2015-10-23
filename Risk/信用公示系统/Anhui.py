#coding=utf-8
__author__ = 'Chen'

import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'gjz':''
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://www.ahcredit.gov.cn/exceptionInfoSelect.jspx',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Magic Browser'}
            )
            result=self.gethtml(req)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            infolist=result.findAll('a',attrs={'target':'_blank'})
            regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
            datelist=result.findAll('li',attrs={'class':'tb-a3'})
            del regIDlist[0]
            del datelist[0]
            l=len(datelist)
            if l==0:break
            br=0
            for i in range(l):
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
                        try:
                            Name=infolist[i].contents[0]
                            regID=regIDlist[i].contents[0]
                            regID=self.dealID(regID)
                            href=infolist[i].get('href')
                            entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                        except Exception:
                            print('error')
                        else:self.PrintInfo(entdict)
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://www.ahcredit.gov.cn'+ent.get('href'),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
            self.gendown(ent,infolist)

if __name__=='__main__':
    location='安徽'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,9),enddate=date.today())
