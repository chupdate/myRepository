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
        page=urllib.request.urlopen(req,timeout=30)
        if compress==True:page=gzip.open(page)
        html=BeautifulSoup(page.read(), 'html.parser')
        return html

    def DownloadInfo(self,Par_Num):
        global id_error
        while True:
            try:
                id=q.get_nowait()
            except Exception:
                break
            infourl=urllib.request.Request(
                url='http://shixin.court.gov.cn/detail?id='+str(id),
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
            try:
                inforesult=self.gethtml(infourl)
                jsonresult=json.loads(str(inforesult))
                self.PrintInfo(id,jsonresult,Par_Num)
            except Exception:
                print('id:%s error' % id)
                iderror.write(str(id)+'\n')
                id_error+=1

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
            print(id,' Complete! ',Par_Num)
        except Exception:
            id_error+=1
            print('id:%s write error' % id)
            iderror.write(str(id)+'\n')

if __name__=='__main__':
    Namearr=[
        'id','iname','cardNum','sexy','age','courtName','areaName',
        'gistId','regDate','caseCode','gistUnit', 'duty','performance','performedPart',
        'unperformPart','disruptTypeName','publishDate','focusNumber'
    ]
    Cookie='_gscu_1049835508=36845235sy4zvm12; __jsluid=a331121232c0e6ad597d641e867df69f; JSESSIONID=2BD0350B90AB82F0F1E7F3D56B032908; __jsl_clearance=1442730121.709|0|vYeWL5M7ARTV%2BT4%2F84eF%2FpUdfak%3D'
    Startdate=date(1900,4,9)
    q=queue.Queue()
    id_error=0
    num=20          #线程数量
    GUP=GetshixinPersonParser()
    iderror=open('D:\\shixin\Person\iderror.txt','a')
    fid=open('D:\\shixin\Person\iderror1.txt','r')
    for line in fid.readlines():
        k=line.find('error')
        if k!=-1:q.put(int(line[3:k-1]))
    fid.close()
    firlist=[]
    for i in range(num):
        firname='D:\\shixin\\Person\\111\\Person_'+str(i+1)+'.txt'
        firlist.append(open(firname,'a'))
        t=threading.Thread(target=GUP.DownloadInfo,args=[i])   #装入子线程队列
        t.setDaemon(True)    #设置守护线程。如果不setDaemon，线程会依次进行，失去多任务处理的功能
        t.start()
    q.join()
    print('Download Complete!')
    print('id_error:',id_error)
    for i in range(num):firlist[i].close()
    iderror.close()




