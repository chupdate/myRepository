#coding=utf-8
__author__ = 'YouYou'
from Crypto.Cipher import AES
from binascii import a2b_hex
import base64
import urllib,urllib2
import json
import random
import cookielib
import re
import os
import time

class MAMAVote():

    def __init__(self):
        self.ck=cookielib.CookieJar()
        cookie_support=urllib2.HTTPCookieProcessor(self.ck)
        self.opener=urllib2.build_opener(cookie_support)
        self.iperror=0

    #获取10分钟随机邮箱
    def downmail(self):
        req=urllib2.Request(
            url='https://10minutemail.net/address.api.php?new=1&_=1446354106613',
            headers={
                'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
            }
        )
        page=urllib2.urlopen(req)
        result=page.read().decode()
        result=json.loads(result)
        mail=result.get('mail_get_mail')
        return mail

    #注册
    #产生随机姓名
    def gername(self):
        long=random.randrange(4,11)   #4-10位的姓名
        name=[]
        for i in range(long):name.append(chr(random.randrange(97,123)))
        name=''.join(name)
        return name
    #产生10位随机密码
    def gerpassword(self):
        password=[]
        password.append('@')
        password.extend(random.sample(range(48,58),3))
        password.extend(random.sample(range(65,91),3))
        password.extend(random.sample(range(97,123),3))
        for i in range(1,len(password)):password[i]=chr(password[i])
        password=''.join(password)
        return password
    #随机出生日期
    def gerbirthday(self):
        year=random.randrange(1990,2001)
        month=random.randrange(1,13)
        day=random.randrange(1,29)
        birthday=str(year)+str(month)+str(day)
        return birthday
    #使用随机邮箱姓名密码出生日期注册
    def regist(self,mail=None,password=None):
        if not mail:self.mail=self.downmail()
        else:self.mail=mail
        print 'Email:',self.mail
        if self.mail:
            if not password:self.password=self.gerpassword()
            else:self.password=password
            print 'Password:',self.password
            self.birthday=self.gerbirthday()
            self.name=self.gername()
            self.gender=random.choice(['f','m'])
            req=urllib2.Request(
                url='https://user.interest.me/common/member/joinEmailProc.html',
                data=urllib.urlencode({
                    'siteCode':'S21',
                    'returnURL':'http://mama.mwave.me/vote',
                    'gender':self.gender,
                    'birthday':self.birthday,
                    'userInfoAgree':'Y',
                    'newsletter':'NNNN',
                    'smsAgree':'NNNN',
                    'tel':'',
                    'agreeChk':'on',
                    'vitalAgreeChk1':'on',
                    'choiceAgreeChk':'on',
                    'email':self.mail,
                    'userName':self.name,
                    'password':self.password,
                    'passwordConfirm':self.password,
                    'extEmail':self.mail,
                }).encode('utf-8'),
                headers={
                    'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
                    'Referer': 'https://user.interest.me/common/member/joinEmailVerify.html?userId=4Wr2o&email=mrj77554%40foxja.com&siteCode=S21&returnURL=http%3A%2F%2Fmama.mwave.me%2Fvote&siteCode=S21&returnURL=http%3A%2F%2Fmama.mwave.me%2Fvote',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Content-Type':'application/x-www-form-urlencoded'
                }
            )
            checkreq=urllib2.Request(
                    url='https://user.interest.me/common/member/checkEmailDuple.json',
                    data=urllib.urlencode({
                        'email':self.mail,
                        'certType':'A6'
                    }).encode('utf-8')
                )
            total=0
            self.logincode='fail'
            while total<=5:
                total+=1
                urllib2.urlopen(req)
                check=urllib2.urlopen(checkreq)
                checkresult=str(check.read())
                reg=r'\"available\":\"(.*)\"'
                pattern=re.compile(reg)
                if pattern.findall(checkresult)[0]=='n':
                    self.logincode='success'
                    print u'注册成功'
                    break
            if self.logincode=='fail':print u'注册失败'

    #登陆
    def login(self,mail=None,password=None):
        if mail:self.mail=mail
        if password:self.password=password
        req=urllib2.Request(
            url='https://user.interest.me/common/login/auth.html',
            data=urllib.urlencode({
                'returnURL':'http://mama.mwave.me/vote',
                'siteCode':'S21',
                'isSaveId':'n',
                'glogin':'',
                'enc':'Y',
                'enc1':self.encrypt(self.mail),
                'enc2':self.encrypt(self.password),
                'layout':'',
                'userId':'',
                'password':''
            }).encode('utf-8'),
            headers={
                'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'http://user.interest.me/common/login/login.html?siteCode=S21&returnURL=http%3A%2F%2Fmama.mwave.me%2Fvote',
                'Host': 'user.interest.me'
            }
        )
        self.opener.open(req)

    #投票
    def vote(self):
        votelist=[list(range(1,6)),list(range(6,11)),list(range(11,16)),
                  list(range(16,21)),[23],list(range(27,33)),list(range(33,38)),[39],list(range(44,50)),
                  list(range(50,55)),list(range(55,60)),list(range(60,65)),list(range(65,70)),list(range(70,75)),
                  list(range(76,80)),[94],[116]]
        votedata=[str(random.choice(ulist)) for ulist in votelist]
        votedata=','.join(votedata)
        cookie=[]
        for item in self.ck:cookie.append(item.name+'='+item.value)
        cookie=';'.join(cookie)
        req=urllib2.Request(
            url='http://mama.mwave.me/setVote.json',
            data=urllib.urlencode({
                'voteData':votedata
            }).encode('utf-8'),
            headers={'Host': 'mama.mwave.me',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'http://mama.mwave.me/vote',
                'Connection': 'keep-alive',
                'Cookie':cookie
            }
        )
        page=urllib2.urlopen(req)
        result=page.read().decode()
        result=json.loads(result)
        if result['response']['CODE']=='success':print u'投票成功'
        elif result['response']['CODE']=='overVotedIp':
            self.iperror=1
            print u'请更换IP'
        else:print u'投票失败'

    #密文处理
    def encrypt(self,text):
        l=len(text)
        m=16-(l % 16)
        for i in range(m):text+=' '
        text=text.encode('utf-8')
        key = a2b_hex('0e0e020104050d0707090b0b0c0d0e0a')
        mode = AES.MODE_CBC
        iv=a2b_hex('0a0e0d070b0a090a07060304030d010b')
        cryptor = AES.new(key,mode,iv)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出可能存在问题
        #统一把加密后的字符串转化为16进制字符串
        enkey=base64.b64encode(self.ciphertext)
        return enkey.decode()

if __name__=='__main__':
    total=0
    while True:
        BTSvote=MAMAVote()
        BTSvote.regist()
        if BTSvote.mail==None:
            print u'请打开10分钟邮箱网站输入验证码，然后重试'
            break
        else:
            BTSvote.login()
            if BTSvote.logincode=='success':
                BTSvote.vote()
                total+=1
        if BTSvote.iperror==1:break
        time.sleep(30)
    os.system('pause')


