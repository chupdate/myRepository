__author__ = 'Chen'
#coding=utf-8
import  urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>27492:break
                req=urllib.request.Request(
                    url='http://gsxt.jxaic.gov.cn/ECPS/enterpriseAbnAction_enterpriseList.action?curr_Page='+str(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('div',attrs={'class':'tb-b'})
                l=len(infolist)
                Namelist=[info.find('a').contents[0] for info in infolist]
                regIDlist=[info.find('li',attrs={'class':'tb-a2'}).contents[0] for info in infolist]
                datelist=[info.find('li',attrs={'class':'tb-a3'}).contents[0] for info in infolist]
                nbxhlist=[info.find('input',attrs={'id':re.compile('nbxh')}).get('value') for info in infolist]
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
                                entdict=dict(Name=Name,regID=regIDlist[i],Date=cdate,nbxh=nbxhlist[i])
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://gsxt.jxaic.gov.cn/ECPS/jyycxxAction_init.action?nbxh='+ent.get('nbxh')
        req=urllib.request.Request(
            url=infourl,
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table').findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='江西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())