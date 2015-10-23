#coding=utf-8
__author__ = 'Chen'
import urllib.request,urllib.parse
import json
import gzip
import threading
from bs4 import BeautifulSoup
import queue

class GetshixinUnitParser:

    def __init__(self):
        self.Cookie='_gscu_1049835508=36845235sy4zvm12; __jsluid=03f4b61df4596d8d27efb900a1f5cc9e; JSESSIONID=0D9D60ECA031328C65A30686614F069E;__jsl_clearance=1442883840.887|0|e%2BxmjbFB%2FJHKNOFDa1QHGYUvdd4%3D'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                    'Accept-Encoding': 'gzip, deflate',
                     'Cookie':self.Cookie,}
        self.Namearr=['iname','cardNum', 'businessEntity','courtName','areaName',
                     'gistId','regDate','caseCode','gistUnit', 'duty','performance','performedPart',
                     'unperformPart','disruptTypeName','publishDate','focusNumber']

    def getpostdata(self,PageNum):
        postdata=urllib.parse.urlencode({
            'currentPage':'%d' % PageNum,
        }).encode('utf-8')   #必须要加.encode
        return postdata

    def gethtml(self,req,compress=False):
        page=urllib.request.urlopen(req, timeout=30)
        if compress:page=gzip.open(page)
        html=BeautifulSoup(page.read(), 'html.parser')
        return html

    def DownloadInfo(self,id,Par_Num):
        global id_error
        infourl=urllib.request.Request(
            url='http://shixin.court.gov.cn/detail?id='+id,
            headers=self.headers
        )
        try:
            inforesult=self.gethtml(infourl,compress=False)
            jsonresult=json.loads(str(inforesult))
            self.PrintInfo(jsonresult,Par_Num)
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
                url='http://shixin.court.gov.cn/unitMore.do',
                data=self.getpostdata(PageNum),
                headers=self.headers
            )
            try:
                result=self.gethtml(req,compress=True)
                result=result.find('table',attrs={'id':'Resultlist'})
                resultlist=result.findAll('tr')[1:]
                for item in resultlist:
                    items=item.findAll('td')
                    id=items[1].find('a').get('id')
                    self.DownloadInfo(id,Par_Num)
                print(PageNum,' Complete!')
            except Exception:
                print('Page:%s error' % PageNum)
                pageerror.write(str(PageNum)+'\n')
                Page_error+=1
            q.task_done()

    def PrintInfo(self,jsonresult,Par_Num):
        global id_error
        f=firlist[Par_Num]
        for i in range(16):
            if  self.Namearr[i] in jsonresult:
                text=jsonresult[self.Namearr[i]]
                if type(text)!=int:
                    f.write(jsonresult[self.Namearr[i]].replace('\n','').replace('\t','').replace('|','').strip()+'|')
                else:
                    f.write(str(text)+'|')
            else:
                f.write('|')
        f.write('\n')

if __name__=='__main__':
    '''
    #使用代理服务器
    proxy_support = urllib.request.ProxyHandler({'http':'http://101.226.249.237'})
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    '''
    q=queue.Queue()
    Page_error,id_error=(0,0)
    num=15
    GUP=GetshixinUnitParser()
    iderror=open('D:\\shixin\\Unit\iderror.txt','a')
    pageerror=open('D:\\shixin\\Unit\pageerror1.txt','a')
    fpage=open('D:\\shixin\\Unit\pageerror.txt','r')
    for line in fpage.readlines():q.put(int(line))
    firlist=[]
    for i in range(num):
        firname='D:\\shixin\\Unit\\Results\\Unit_'+str(i+1)+'.txt'
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


