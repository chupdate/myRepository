__author__ = 'Chen'
#coding=utf-8
#被列入经营异常名录日期由远及近
#作出决定机关（列入和移出）
#出现频繁访问错误
import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNos':'%d'% pageNos,
            'pageNo':'%d' % (pageNos-1),
            'pageSize':'10',
            'clear':'',
            'querystr':'请输入企业名称或注册号'
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>8921:break
                req=urllib.request.Request(
                    url='http://qyxy.baic.gov.cn/dito/ditoAction!ycmlFrame.dhtml',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                             'Cookie':' JSESSIONID=ZyqLW3VQJpmG2jvYxmdB5z0rmfMQ8D89f1BTv4PQ91Fn5Qjy70Wh!-2120185996; BIGipServerpool_xy3_web=1125492928.17183.0000'}
                )
                result=self.gethtml(req)
                table=result.find('table')
                infolist=table.findAll('td')
                l=len(infolist)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(2,l,3):
                    try:
                        cdate=infolist[i].contents[0]
                        cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=infolist[i-2].find('a').contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=infolist[i-1].contents[0]
                                EntInfo=infolist[i-2].find('a').get('onclick')
                                reg=r'\'([A-Za-z0-9]{32})\''
                                pattern=re.compile(reg)
                                li=pattern.findall(EntInfo)
                                entId=li[0]
                                entdict=dict(Name=Name,regID=regID,entId=entId)
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
                if br==1:break

    def PrintInfo(self,ent,f):
        req=urllib.request.Request(
            url='http://qyxy.baic.gov.cn/gsgs/gsxzcfAction!list_jyycxx.dhtml?entId='+\
                ent.get('entId')+'&clear=true&timeStamp=1',
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Cookie':'JSESSIONID=ZyqLW3VQJpmG2jvYxmdB5z0rmfMQ8D89f1BTv4PQ91Fn5Qjy70Wh!-2120185996; BIGipServerpool_xy3_web=1125492928.17183.0000'}
        )
        inforesult=self.gethtml(req)
        info=inforesult.find('body').findAll('td')
        l=int(len(info)/7)
        for j in range(l):
            f.write(ent.get('Name')+'|')
            f.write(ent.get('regID')+'|')
            for k in range(6):
                if k!=3:
                    i=j*7+k
                    infostr=info[i].contents
                    if infostr:
                        infostr=infostr[0]
                        f.write(infostr.replace('\n','').strip()+'|')
                    else:
                        f.write('|')
            i=j*7+3
            infostr=info[i].contents
            if infostr:
                infostr=infostr[0]
                f.write(infostr.replace('\n','').strip()+'|')
            else:
                f.write('|')
            f.write('\n')

if __name__=='__main__':
    location='北京'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())