__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser
import bs4

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'gjz':'',
            'Content-Length': '13',
            'Connection':'keep-alive'
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://gxqyxygs.gov.cn/exceptionInfoSelect.jspx',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
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
                            href=infolist[i].get('href')
                            entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                            self.PrintInfo(entdict)
                        except Exception:
                            print('error')
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://gxqyxygs.gov.cn'+ent.get('href')
        inforesult=self.gethtml(infourl)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
            self.gendown(ent,infolist)

if __name__=='__main__':
    location='广西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,9),enddate=date.today())