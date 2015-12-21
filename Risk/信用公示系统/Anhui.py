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
            if pageNos>19337:break
            try:
                req=urllib.request.Request(
                    url='http://www.ahcredit.gov.cn/exceptionInfoSelect.jspx',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('a',attrs={'target':'_blank'})
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
                                Name=infolist[i].contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=regIDlist[i].contents[0]
                                regID=self.dealID(regID)
                                href=infolist[i].get('href')
                                entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=urllib.request.Request(
            url='http://www.ahcredit.gov.cn'+ent.get('href'),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='安徽'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())
