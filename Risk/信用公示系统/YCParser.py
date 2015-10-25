__author__ = 'Chen'
import urllib.request
from bs4 import BeautifulSoup
import re

class YCParser():

    def gethtml(self,req,retries=3,timeout=15):
        try:
            page=urllib.request.urlopen(req,timeout=timeout)
            html=BeautifulSoup(page.read(),"html.parser")
            return html
        except Exception:
            if retries>0:return self.gethtml(req, retries-1)
            else:raise Exception

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
            self.f.write(ent.get('Name').replace('\n','').strip()+'|')
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

