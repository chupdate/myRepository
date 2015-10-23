__author__ = 'Chen'
#coding=utf-8
#如果抓取异常，手动更换Cookie
import urllib.parse,urllib.request
import re
from datetime import *
from YCParser import YCParser
import json
import time

class GetYCParser(YCParser):

    def getinfopostdata(self,nbxh):
        postdata=urllib.parse.urlencode({
            'c':'0',
            't':'33',
            'nbxh':nbxh
        }).encode('utf-8')
        return postdata

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d'% pageNos,
            'pageSize':'50'
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        time.sleep(3)
        pageNos=0
        self.cookie='JSESSIONID=cx8GWklKDV1zsbzCPfTd0yGsvr23JpDqklJgXVzRSLLVdJ5vn5LN!-148777718!1654306382; CNZZDATA5828332=cnzz_eid%3D1496011142-1445223064-%26ntime%3D1445223064'
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://gsxt.gzgs.gov.cn/addition/search!searchJyyc.shtml',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Magic Browser',
                         'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
                         'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                         'Accept-Encoding':'gzip, deflate',
                         'X-Requested-With':'XMLHttpRequest',
                         'Referer':'http://gsxt.gzgs.gov.cn/addition/jyyc.jsp',
                         'Cookie':self.cookie,
                         'Content-Length':'20'
                        }
            )
            result=self.gethtml(req,timeout=100)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % pageNos)
            result=json.loads(str(result))
            result=result['data']
            br=0
            for res in result:
                cdate=str(res['lrrq'])
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
                        entdict=dict(Name=res['qymc'],nbxh=res['nbxh'],regID=res['zch'],date=cdate)
                        self.PrintInfo(entdict,self.f)
            if br==1:break

    def PrintInfo(self,ent,f):
        #time.sleep(3)
        req=urllib.request.Request(
            url='http://gsxt.gzgs.gov.cn/nzgs/search!searchData.shtml',
            data=self.getinfopostdata(ent['nbxh']),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
                     'Host':'gsxt.gzgs.gov.cn',
                     'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
                     'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                     'Accept-Encoding':'gzip, deflate',
                     'X-Requested-With':'XMLHttpRequest',
                     'Referer':'http://gsxt.gzgs.gov.cn/nzgs/index.jsp',
                     'Cookie':self.cookie,
                     'Content-Length':'78',
                     'Connection':'keep-alive',
                     'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=json.loads(str(inforesult))['data']
            for info in infolist:
                f.write(ent.get('Name').replace('\n','').strip()+'|')
                f.write(ent.get('regID')+'|')
                f.write(str(info['rownum'])+'|')
                if info['lryy']:f.write(info['lryy'])
                f.write('|')
                f.write(info['lrrq']+'|')
                if info['ycyy']:f.write(info['ycyy'])
                f.write('|')
                if info['ycrq']:f.write(info['ycrq'])
                f.write('|')
                f.write(info['zcjdjg']+'|')
                f.write('\n')

if __name__=='__main__':
    location='贵州'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,10),enddate=date.today()-timedelta(days=0))