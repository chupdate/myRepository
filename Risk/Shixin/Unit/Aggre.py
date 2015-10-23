#coding=utf-8
__author__ = 'LittleYou'
import os

if __name__=='__main__':
    rs='D:/shixin/Unit/Results/'
    dirlist=os.listdir(rs)
    fw=open('D:/shixin/Unit/失信企业整理.txt','a')
    for dirr in dirlist:
        f=open(rs+dirr,'r')
        for line in f.readlines():fw.write(line)
        f.close()
    fw.close()