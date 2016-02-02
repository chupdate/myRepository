__author__ = 'Chen'
#coding=utf-8
import urllib.parse,urllib.request

import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'captcha':'',
            'condition.pageNo':'%d'% pageNos,
            'condition.insType':'',
            'session.token':self.token,
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        self.token='14d90848-8f48-405f-be20-7a9639be9d6a'
        while True:
            try:
                pageNos+=1
                if pageNos>6934:break
                req=urllib.request.Request(
                    url='http://gsxt.ynaic.gov.cn/notice/search/ent_except_list',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                             'Cookie':'JSESSIONID_NOTICE=FGfTWlTD5p7hf2kWLwxyPVJ8DHkBTBvNtgx3LQTD3hsyML2NYqJP!-1915091912; notice=20111111; CNZZDATA1000298231=721015559-1453691075-http%253A%252F%252Fgsxt.saic.gov.cn%252F%7C1453696742'}
                )
                result=self.gethtml(req)
                infolist=result.find('table',attrs={'class':'list-table'}).findAll('td')
                l=int(len(infolist)/3)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for j in range(l):
                    try:
                        i=j*3+2
                        cdate=str(infolist[i].contents[0])
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
                                Name=infolist[i-2].find('a').contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=infolist[i-1].contents[0]
                                href=infolist[i-2].find('a').get('href')
                                entdict=dict(Name=Name,regID=regID,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl=ent.get('href')
        inforesult=self.gethtml(infourl)
        infolist=inforesult.find('table',attrs={'id':'exceptTable'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='云南'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,11,1),enddate=date.today()-timedelta(days=0))
