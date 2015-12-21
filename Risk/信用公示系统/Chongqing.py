__author__ = 'Chen'
#coding=utf-8
import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser
import json

class GetYCParser(YCParser):

    def getinfopostdata(self,id,type,name,entId):
        if name:name=name.encode('utf-8')
        postdata=urllib.parse.urlencode({
            'id':id,
            'type':type,
            'name':name,
            'seljyyl':'true',
            'entId':entId
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>7824:break
                url='http://gsxt.cqgs.gov.cn/search_searchjyyc.action?currentpage='+str(pageNos)+'&itemsperpage=10'
                result=self.gethtml(url)
                result=json.loads(str(result))
                br=0
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                for jyyc in result['jyyclist']:
                    try:
                        cdate=jyyc['_date']
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
                                Name=jyyc.get('_name').replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,regID=jyyc.get('_regCode'),Date=cdate,ID=jyyc.get('_pripid'),entType=jyyc.get('_entType'))
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,jyyc)
                        continue
            if br==1:break

    def PrintInfo(self,ent,f):
        #post方法获取type值，然后采用get方法
        req=urllib.request.Request(
            url='http://gsxt.cqgs.gov.cn/search_ent',
            data=self.getinfopostdata(ent.get('regID'),ent.get('entType'),ent.get('Name'),ent.get('ID')),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req).find('body',attrs={'ng-controller':'frameCtrl'})
        inforesult=str(inforesult)
        reg=r'data-type=\"(\d)*\"'
        pattern=re.compile(reg)
        type=pattern.findall(inforesult)[0]
        infourl='http://gsxt.cqgs.gov.cn/search_getEnt.action?entId='+ent.get('ID')+'&id='+ent.get('regID')+'&type='+type
        inforesult=str(self.gethtml(infourl))
        #提取Entity页面内的经营异常信息
        reg=r'"qyjy":\[(.*)\]'
        pattern=re.compile(reg)
        qyjy=pattern.findall(inforesult)[0]
        reg=r'\{(.*?)\}'
        pattern=re.compile(reg)
        infolist=pattern.findall(qyjy)
        l=len(infolist)
        for i in range(l):
            if ent.get('Name'):f.write(ent.get('Name')+'|')
            else:f.write('|')
            if ent.get('regID'):f.write(ent.get('regID')+'|')
            else:f.write('|')
            f.write(str(i+1)+'|')
            info=infolist[i]
            reg=r'"specause":"(.*?)"'
            pattern=re.compile(reg)
            inreason=pattern.findall(info)
            f.write(inreason[0]+'|')
            reg=r'"abntime":"(.*?)"'
            pattern=re.compile(reg)
            intime=pattern.findall(info)
            f.write(intime[0]+'|')
            reg=r'"remexcpres":"(.*?)"'
            pattern=re.compile(reg)
            outreason=pattern.findall(info)
            if outreason:f.write(outreason[0])
            f.write('|')
            reg=r'"remdate":"(.*?)"'
            pattern=re.compile(reg)
            outtime=pattern.findall(info)
            if outtime:f.write(outtime[0])
            f.write('|')
            reg=r'"decorg":"(.*?)"'
            pattern=re.compile(reg)
            org=pattern.findall(info)
            f.write(org[0]+'|')
            f.write('\n')


if __name__=='__main__':
    location='重庆'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())
