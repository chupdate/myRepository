__author__ = 'Han'
#coding=utf-8

import jieba

if __name__=='__main__':
    seq=list(jieba.cut('高士达（福建）房地产开发有限公司'))
    while '(' in seq:seq.remove('(')
    while '（'in seq:seq.remove('（')
    while ')' in seq:seq.remove(')')
    while '）' in seq:seq.remove('）')
    print(seq)

