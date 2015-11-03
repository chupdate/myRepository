__author__ = 'Han'
#coding=utf-8
import jieba
import os

def findkeywords(name):
    seq=list(jieba.cut(name))
    while '(' in seq:seq.remove('(')
    while '（'in seq:seq.remove('（')
    while ')' in seq:seq.remove(')')
    while '）' in seq:seq.remove('）')
    while '[' in seq:seq.remove('[')
    while ']' in seq:seq.remove(']')
    return seq

if __name__=='__main__':
    f=open('D:\\nametest1.txt','r')
    #de1=open('D:\\Test处理.txt','w')
    for line in f.readlines():
        name=line.replace('/n','').strip()
        if len(name)<=3:continue
        keywords=findkeywords(name)

        l=len(keywords)
        if (l==0) or (l==1):
            print('name=',name,'keywords=',''.join(keywords),'l=',l)
            con=input('是否保留Y/N')
            if con=='N':continue
        print('name=%s\nkeywords=%s' % (name,keywords))
        os.system('pause')
    f.close()
