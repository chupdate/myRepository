__author__ = 'Chen'
#coding=utf-8
import urllib.parse,urllib.request
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
            try:
                pageNos+=1
                if pageNos>51451:break
                req=urllib.request.Request(
                    url='http://xyjg.egs.gov.cn/ECPS_HB/exceptionInfoSelect.jspx',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                Namelist0=result.findAll('li',attrs={'class':'tb-a1'})[1:]
                Namelist=[Name.find('a').contents[0] for Name in Namelist0]
                regIDlist0=result.findAll('li',attrs={'class':'tb-a2'})[1:]
                pattern=re.compile(r'(\d*)')
                regIDlist=[pattern.findall(regID.contents[0])[0] for regID in regIDlist0]
                datelist0=result.findAll('li',attrs={'class':'tb-a3'})[1:]
                datelist=[dat.contents[0] for dat in datelist0]
                hreflist0=result.findAll('li',attrs={'class':'tb-a1'})[1:]
                hreflist=[href.find('a').get('href') for href in hreflist0]
                l=len(datelist)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        cdate=str(datelist[i])
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
                                Name=Namelist[i].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,regID=regIDlist[i],Date=cdate,href=hreflist[i])
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://xyjg.egs.gov.cn'+ent.get('href')
        inforesult=self.gethtml(infourl)
        infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='湖北'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())