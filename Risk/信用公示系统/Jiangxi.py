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
            pageNos+=1
            req=urllib.request.Request(
                url='http://gsxt.jxaic.gov.cn/ECPS/enterpriseAbnAction_enterpriseList.action?curr_Page='+str(pageNos),
                headers={'User-Agent':'Magic Browser'}
            )
            result=self.gethtml(req)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            infolist=result.findAll('div',attrs={'class':'tb-b'})
            l=len(infolist)
            if l==0:break
            Namelist=[info.find('a').contents[0] for info in infolist]
            regIDlist=[info.find('li',attrs={'class':'tb-a2'}).contents[0] for info in infolist]
            datelist=[info.find('li',attrs={'class':'tb-a3'}).contents[0] for info in infolist]
            nbxhlist=[info.find('input',attrs={'id':re.compile('nbxh')}).get('value') for info in infolist]
            br=0
            for i in range(l):
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
                        entdict=dict(Name=Namelist[i],regID=regIDlist[i],Date=cdate,nbxh=nbxhlist[i])
                        self.PrintInfo(entdict)
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://gsxt.jxaic.gov.cn/ECPS/jyycxxAction_init.action?nbxh='+ent.get('nbxh')
        req=urllib.request.Request(
            url=infourl,
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=inforesult.find('table').findAll('td')
            self.gendown(ent,infolist)

if __name__=='__main__':
    location='江西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,9),enddate=date.today())