#coding=utf-8
__author__ = 'Chen'
import urllib.parse,urllib.request
import gzip
import json
import threading
from bs4 import BeautifulSoup
from datetime import *
import queue


class GetshixinPersonParser:

    def getpostdata(self,PageNum):
        postdata=urllib.parse.urlencode({
            'currentPage':'%d'% PageNum,
        }).encode('utf-8')
        return postdata

    def gethtml(self,req,compress=False):
        page=urllib.request.urlopen(req,timeout=45)
        if compress==True:page=gzip.open(page)
        html=BeautifulSoup(page.read(), 'html.parser')
        return html

    def DownloadInfo(self,id,Par_Num):
        global id_error
        try:
            infourl=urllib.request.Request(
                url='http://shixin.court.gov.cn/detail?id='+id,
                headers={
                     'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'shixin.court.gov.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://shixin.court.gov.cn/personMore.do',
                     'Cookie':Cookie,
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0'})
            inforesult=self.gethtml(infourl)
            jsonresult=json.loads(str(inforesult))
            self.PrintInfo(id,jsonresult,Par_Num)
        except Exception:
            print('id:%s error' % id)
            iderror.write(id+'\n')
            id_error+=1

    def Shixin_Get(self,Par_Num):
        global Page_error
        while True:
            try:
                PageNum=q.get_nowait()
            except Exception:
                break
            req=urllib.request.Request(
                url='http://shixin.court.gov.cn/personMore.do',
                data=self.getpostdata(PageNum),
                headers={
                     'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'shixin.court.gov.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://shixin.court.gov.cn/personMore.do',
                     'Cookie':Cookie,
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0'}
            )
            try:
                result=self.gethtml(req,compress=True)
                result=result.find('table',attrs={'id':'Resultlist'})
                resultlist=result.findAll('tr')[1:]
                for item in resultlist:
                    items=item.findAll('td')
                    cdate=items[3].contents[0]
                    year=int(cdate[0:4])
                    month=int(cdate[5:7])
                    day=int(cdate[8:10])
                    cdate=date(year,month,day)
                    if cdate>=Startdate:
                        id=items[1].find('a').get('id')
                        self.DownloadInfo(id,Par_Num)
                print(PageNum,' Complete!',' ',Par_Num)
            except Exception:
                print('Page:%s error' % PageNum)
                pageerror.write(str(PageNum)+'\n')
                Page_error+=1
            q.task_done()

    def PrintInfo(self,id,jsonresult,Par_Num):
        global id_error
        f=firlist[Par_Num]
        try:
            for i in range(16):
                if Namearr[i] in jsonresult:
                    text=jsonresult[Namearr[i]]
                    if type(text)!=int:
                        f.write(jsonresult[Namearr[i]].replace('\n','').replace('\t','').replace('||','').strip()+'||')
                    else:
                        f.write(str(text)+'||')
                else:
                    f.write('||')
            f.write('\n')
        except Exception:
            id_error+=1
            print('id:%s write error' % id)
            iderror.write(id+'\n')

if __name__=='__main__':
    Namearr=[
        'id','iname','cardNum','sexy','age','courtName','areaName',
        'gistId','regDate','caseCode','gistUnit', 'duty','performance','performedPart',
        'unperformPart','disruptTypeName','publishDate','focusNumber'
    ]
    Cookie='_gscu_1049835508=36845235sy4zvm12; __jsluid=bbf29994690d78377764bba905a2d343; JSESSIONID=17E046A0692EB3EB893DD55A7BC5AE0B; __jsl_clearance=1442728476.223|0|UgvuRR%2Fz3jz02wO1zmK6K7WmTfQ%3D'
    Startdate=date(1900,4,9)
    q=queue.Queue()
    Page_error,id_error=(0,0)
    num=3          #线程数量
    GUP=GetshixinPersonParser()
    iderror=open('D:\\shixin\Person\iderror.txt','a')
    pageerror=open('D:\\shixin\Person\pageerror1.txt','a')
    fpage=open('D:\\shixin\Person\Errorpages.txt','r')
    for line in fpage.readlines():q.put(int(line))
    fpage.close()
    firlist=[]
    for i in range(num):
        firname='D:\\shixin\\Person\\111\\Person_'+str(i+1)+'.txt'
        firlist.append(open(firname,'a'))
        t=threading.Thread(target=GUP.Shixin_Get,args=[i])   #装入子线程队列
        t.setDaemon(True)    #设置守护线程。如果不setDaemon，线程会依次进行，失去多任务处理的功能
        t.start()
    q.join()
    print('Download Complete!')
    print('Page_error:',Page_error)
    print('id_error:',id_error)
    for i in range(num):firlist[i].close()
    iderror.close()
    pageerror.close()




