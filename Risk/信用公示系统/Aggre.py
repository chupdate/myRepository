__author__ = 'Han'
#coding=utf-8
import os

rs='D:/GSXTresult/'
dirlist=os.listdir(rs)
fw=open('D:/GSXT整理.txt','w')

for dirr in dirlist:
    f=open(rs+dirr,'r')
    k=dirr.find('.')
    prov=dirr[:k]
    for line in f.readlines():
        k=line.find('|')
        head=line[:k]
        if len(head)>=4:fw.write(line.replace('\n','')+'|'+prov+'\n')
    f.close()
fw.close()
