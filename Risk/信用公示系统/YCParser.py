__author__ = 'Chen'
import urllib.request
from urllib.error import HTTPError
from urllib.request import Request
from bs4 import BeautifulSoup
import re


class YCParser():

    def __init__(self):
        self.opener=urllib.request.build_opener(self.RedirectHandler)
        self.namecheck=['摊']

    #解决自动重定向问题
    class RedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            m = req.get_method()
            if (not (code in (301, 302, 303, 307) and m in ("GET", "HEAD")
                or code in (301, 302, 303, 307) and m == "POST")):
                raise HTTPError(req.full_url, code, msg, headers, fp)
            newurl = newurl.replace(' ', '%20')
            CONTENT_HEADERS = ("content-length", "content-type")
            newheaders = dict((k, v) for k, v in req.headers.items()
                              if k.lower() not in CONTENT_HEADERS)
            return Request(newurl,
                           headers=newheaders,
                           origin_req_host=req.origin_req_host,
                           unverifiable=True)

    def gethtml(self,req,retries=3,timeout=15):
        try:
            page=self.opener.open(req,timeout=timeout)
            html=BeautifulSoup(page.read(),"html.parser")
            return html
        except Exception as err:
            if retries>0:return self.gethtml(req, retries-1)
            else:raise err

    def GetYC(self,location,startdate,enddate,fmode='w',pagemode='w',itemmode='w'):
        self.f=open('D:\\GSXT\\'+location+'.txt',fmode)
        self.pageerror=open('D:\\GSXT\\ErrorPages\\'+location+'.txt',pagemode)
        self.itemerror=open('D:\\GSXT\\ErrorItems\\'+location+'.txt',itemmode)
        self.pageerrornum=0
        self.itemerrornum=0
        self.getentlist(startdate,enddate)
        self.f.close()
        self.pageerror.close()
        print('pageerrornum=',self.pageerrornum)
        print('itemerrornum=',self.itemerrornum)

    def printpageerror(self,pageNos):
        print('Page %d Failed' % pageNos)
        self.pageerrornum+=1
        self.pageerror.write(str(pageNos)+'\n')

    def printitemerror(self,pageNos,i):
        print('item error')
        self.itemerrornum+=1
        self.itemerror.write(str(pageNos)+','+str(i)+'\n')

    def dealID(self,regID):
        reg=r'(\d+)'
        pattern=re.compile(reg)
        regID=pattern.findall(regID)[0]
        return regID

    def gendown(self,ent,infolist):
        l=int(len(infolist)/6)
        for j in range(l):
            self.f.write(ent.get('Name')+'|')
            self.f.write(ent.get('regID').strip()+'|')
            for k in range(6):
                i=j*6+k
                infostr=infolist[i].contents
                if infostr:
                    infostr=infostr[0]
                    self.f.write(infostr.replace('\n','').strip()+'|')
                else:
                    self.f.write('|')
            self.f.write('\n')

    def checkname(self,name):
        if (len(name)<=3) or (name[-1] in self.namecheck):return False
        else:return True
