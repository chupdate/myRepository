__author__ = 'Chen'
#coding=utf-8
#如果读取post异常，使用浏览器刷新网页或“编辑与重发”
import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def changedate(self,fdate):   #处理日期格式
        if (fdate.find('年')==-1)&(fdate.find('-')==-1):
            cdate=date(int(fdate[0:4]),int(fdate[4:6]),int(fdate[6:8]))
        else:
            if fdate.find('-')!=-1:
                fdate=fdate.replace('-','年',1)
                fdate=fdate.replace('-','月',1)
                fdate=fdate+'日'
            reg=r'年(.*?)月'
            pattern=re.compile(reg)
            month=int(pattern.findall(fdate)[0])
            reg=r'月(.*?)日'
            pattern=re.compile(reg)
            day=int(pattern.findall(fdate)[0])
            cdate=date(int(fdate[0:4]),month,day)
        return cdate

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'searchContent':'',
            'page':'%d'% pageNos
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://tjcredit.gov.cn/platform/saic/exclist.ftl',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Magic Browser'}
            )
            result=self.gethtml(req)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            infolist=result.findAll('li',attrs={'class':'tb-a1'})
            datelist=result.findAll('li',attrs={'class':'tb-a3'})
            del infolist[0]
            del datelist[0]
            l=len(datelist)
            if l==0:break
            k=0
            for i in range(l):
                cdate=str(datelist[i].contents[0])
                cdate=self.changedate(cdate)
                if (cdate>=startdate)&(cdate<=enddate):
                    Name=infolist[i].find('a').contents[0]
                    href=infolist[i].find('a').get('href')
                    reg=r'entId=(.*)'
                    pattern=re.compile(reg)
                    entId=pattern.findall(href)[0]
                    entdict=dict(Name=Name,entId=entId)
                    self.PrintInfo(entdict,self.f)
                if cdate<startdate:
                    k=1
                    break
            if k==1:break

    def PrintInfo(self,ent,f):
        #取得注册号
        infourl='http://tjcredit.gov.cn/platform/saic/viewBaseExc.ftl?entId='+ent.get('entId')
        inforesult=self.gethtml(infourl)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            id=inforesult.findAll('span')[1].contents[0][5:]
        #取得经营异常信息
            infourl='http://tjcredit.gov.cn/platform/saic/baseInfo.json?entId='+ent.get('entId')+'&departmentId=scjgw&infoClassId=qyjyycmlxx'
            inforesult=self.gethtml(infourl)
            if inforesult=='Get Failed':
                print('Item Failed')
            else:
                infolist=inforesult.findAll('td',attrs={'class':''})
                l=int(len(infolist)/6)
                for j in range(l):
                    f.write(ent.get('Name')+'|')
                    f.write(id+'|')
                    for k in range(6):
                        i=j*6+k
                        infostr=infolist[i].contents
                        if infostr:
                            infostr=infostr[0]
                            if i==2:f.write(str(self.changedate(str(infostr))))
                            else:f.write(infostr.replace('\n','').strip())
                        f.write('|')
                    f.write('\n')


if __name__=='__main__':
    location='天津'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,8),enddate=date.today()-timedelta(days=1))
