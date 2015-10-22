__author__ = 'XinYi'
#coding=utf-8
import urllib.parse,urllib.request
import json
import time
import random
import queue
import gzip

def vote(proxy):
    global votes
    global uid
    global badlist
    print(proxy)
    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
    try:
        opener.open('http://www.baidu.com',timeout=2)
    except Exception:
        print('代理IP不可用')
        badlist.append(hea(proxy))
    else:
        print('代理IP可用')
        uid_test=list(uid)
        pos=random.randrange(20)
        if pos>=8:pos+=16
        k=random.randrange(6)
        if k<2:uid_test[pos]=chr(random.randrange(97,123))
        else:uid_test[pos]=chr(random.randrange(48,58))
        uid_test=''.join(uid_test)
        req=urllib.request.Request(
            url='http://ema-funnel.mtvnservices.com/api/v2/mtvema.com/collections/ema2015-vote-china/entries',
            data=urllib.parse.urlencode({
                'ema15-2-asia':'ema15-bts',
                'ema15-9-locale':'CN',
                'ema2015-vote_id':uid_test+'_ema15-2-asia'
            }).encode('utf-8')
        )
        try:
            page=opener.open(req,timeout=15)
            result=page.read()
            href=json.loads(result.decode())[0]['link']['href']
        except Exception as err:
            #print(err)
            if str(err)=='[WinError 10054] 远程主机强迫关闭了一个现有的连接。':
                print('远程主机强迫关闭了现有连接,投票失败')
            else:
                print('服务器未响应，投票失败')
            badlist.append(hea(proxy))
        else:
            try:
                time.sleep(3)
                opener.open(href,timeout=15)
            except Exception as err:
                print(err)
                badlist.append(hea(proxy))
            else:
                votes+=1
                print('投票成功,已投 %d 票' % votes)
                print(href)
                uid=uid_test


def hea(proxy):
    k=proxy[4:].find('.')+4
    return proxy[:k]

if __name__=='__main__':
    votes=0
    uid='3eba37b4-7420-11e5-8019-1f1a03645225'
    while True:
        url='http://dev.kuaidaili.com/api/getproxy/?orderid=984507365209020&num=1000' \
            '&protocol=1&method=2&an_ha=1&quality=1&sort=0&format=json&sep=1&sp1=1&sp2=1'
        page=urllib.request.urlopen(url)
        jsonresult=json.loads(page.read().decode())
        proxy_list=jsonresult['data']['proxy_list']
        badlist=[]
        rand_proxy_list=random.sample(proxy_list,1000)
        for proxy in rand_proxy_list:
            if hea(proxy) not in badlist:vote(proxy)


