__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse

import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'num':'%d'% pageNos,
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>9411:break
                req=urllib.request.Request(
                    url='http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/getJyycmlxx.action',
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
                        cdate=datelist[i].contents[0].replace('\n','').strip()
                        cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=infolist[i].contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=regIDlist[i].contents[0]
                                Name=Name.replace('\n','').strip()
                                regID=regID.replace('\n','').strip()
                                info=infolist[i].get('onclick')
                                reg=r'detailYcjyml\(\'(.*?)\','
                                pattern=re.compile(reg)
                                pri=pattern.findall(info)[0]
                                reg=r'\'(\d{4})\''
                                pattern=re.compile(reg)
                                type=pattern.findall(info)[0]
                                entdict=dict(Name=Name.replace('\n','').strip(),regID=regID.replace('\n','').strip(),Date=cdate,pri=pri,type=type)
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent,f):
        infourl='http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/getJyycxxAction.action?pripid='+ent['pri']+'&type='+ent['type']
        inforesult=str(self.gethtml(infourl))
        reg=r'jyyc_paging\(\[(.*?)\]'
        pattern=re.compile(reg)
        info=pattern.findall(inforesult)[0]
        reg=r'\{.*?\}'
        pattern=re.compile(reg)
        infolist=pattern.findall(info)
        l=len(infolist)
        for i in range(l):
            f.write(ent.get('Name')+'|')
            f.write(ent.get('regID').strip()+'|')
            f.write(str(i+1)+'|')
            infdict=eval(infolist[i])
            f.write(infdict['specauseName']+'|')
            f.write(infdict['abnDate']+'|')
            if infdict['remexcpresName']:f.write(infdict['remexcpresName'])
            f.write('|')
            if infdict['remDate']:f.write(infdict['remDate'])
            f.write('|')
            f.write(infdict['lrregorgName']+'|')
            f.write('\n')

if __name__=='__main__':
    location='辽宁'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,10),enddate=date.today()-timedelta(days=0))