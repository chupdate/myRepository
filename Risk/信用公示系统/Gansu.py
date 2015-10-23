__author__ = 'Chen'
#coding=utf-8
import urllib.parse,urllib.request
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            req=urllib.request.Request(
               url='http://xygs.gsaic.gov.cn/gsxygs/pub!getCommon.do?parm=excplist&queryVal=20%&pageno='+str(pageNos),
               headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate'}
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
                cdate=datelist[i].contents[0].strip()
                cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        Name=infolist[i].contents[0]
                        regID=regIDlist[i].contents[0]
                        href=infolist[i].get('href')
                        entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                        self.PrintInfo(entdict)
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://xygs.gsaic.gov.cn'+ent.get('href'),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
                    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.find('tr',attrs={'id':'excp_tr1'}).findAll('td')
            self.gendown(ent,infolist)

if __name__=='__main__':
    location='甘肃'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,9,20),enddate=date.today()-timedelta(days=0))

