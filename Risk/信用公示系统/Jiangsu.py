__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse

import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'pageSize':'10'
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,ID,ORG,SeqID):
        postdata=urllib.parse.urlencode({
            'showRecordLine':'1',
            'specificQuery':'commonQuery',
            'corp_org':ORG,
            'corp_id':ID,
            'corp_seq_id':SeqID,
            'propertiesName':'abnormalInfor',
            'pageNo':'1',
            'pageSize':'5'
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>57391:break
                req=urllib.request.Request(
                    url='http://www.jsgsj.gov.cn:58888/province/NoticeServlet.json?QueryExceptionDirectory=true',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                result=str(result)
                reg=r'"C1":"(.*?)"'
                pattern=re.compile(reg)
                Namelist=pattern.findall(result)
                reg=r'"C2":"(.*?)"'
                pattern=re.compile(reg)
                regIDlist=pattern.findall(result)
                reg=r'"C3":"(.*?)"'
                pattern=re.compile(reg)
                datelist=pattern.findall(result)
                reg=r'"CORP_ID":(\d*)'
                pattern=re.compile(reg)
                IDlist=pattern.findall(result)
                reg=r'"CORP_ORG":(\d*)'
                pattern=re.compile(reg)
                ORGlist=pattern.findall(result)
                reg=r'"SEQ_ID":(\d*)'
                pattern=re.compile(reg)
                SeqIDlist=pattern.findall(result)
                l=len(datelist)
            except Exception:
                self.printpageerror(pageNos)
                break
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        sdate=datelist[i]
                        cdate=date(int(sdate[0:4]),int(sdate[5:7]),int(sdate[8:10]))
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=Namelist[i].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,regID=regIDlist[i],Date=cdate,ID=IDlist[i],ORG=ORGlist[i],SeqID=SeqIDlist[i])
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent,f):
        req=urllib.request.Request(
            url='http://www.jsgsj.gov.cn:58888/ecipplatform/commonServlet.json?commonEnter=true',
            data=self.getinfopostdata(ent.get('ID'),ent.get('ORG'),ent.get('SeqID')),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=str(self.gethtml(req))
        #提取Entity页面内的经营异常信息
        reg=r'"items":\[(.*)\]'
        pattern=re.compile(reg)
        items=pattern.findall(inforesult)[0]
        reg=r'\{(.*?)\}'
        pattern=re.compile(reg)
        infolist=pattern.findall(items)
        l=len(infolist)
        for i in range(l):
            f.write(ent.get('Name')+'|')
            f.write(ent.get('regID')+'|')
            f.write(str(i+1)+'|')
            inforesult=infolist[i]
            reg=r'"C1":"(.*?)"'
            pattern=re.compile(reg)
            inreason=pattern.findall(inforesult)
            f.write(inreason[0]+'|')
            f.write(str(ent.get('Date'))+'|')
            reg=r'"C3":(.*?)'
            pattern=re.compile(reg)
            outreason=pattern.findall(inforesult)
            if outreason!="null":f.write(outreason[0])
            f.write('|')
            reg=r'"C4":(.*?)'
            pattern=re.compile(reg)
            outdate=pattern.findall(inforesult)
            if outdate!="null":f.write(outdate[0])
            f.write('|')
            reg=r'"C5":"(.*?)"'
            pattern=re.compile(reg)
            JG=pattern.findall(inforesult)
            f.write(JG[0]+'|')
            f.write('\n')

if __name__=='__main__':
    location='江苏'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today()-timedelta(days=0))

