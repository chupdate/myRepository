__author__ = 'Han'
#coding=utf-8
import os

rs='D:/shixin/Person/111/'
dirlist=os.listdir(rs)
fw=open('D:/shixin/Person/失信人整理.txt','a')

for dirr in dirlist:
    f=open(rs+dirr,'r')
    for line in f.readlines():fw.write(line)
    f.close()
fw.close()
