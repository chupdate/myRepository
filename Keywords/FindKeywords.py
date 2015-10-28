__author__ = 'Han'
#coding=utf-8
import jieba

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
    f=open('C:\\Users\\Han\\Desktop\\手动抓取.txt','r')
    de1=open('C:\\Users\\Han\\Desktop\\处理1.txt','w')
    deallist=['店','室','城','场','站','房','馆','部','厅','院','园','屋','社','行','处','所','摊']
    total=0
    for line in f.readlines():
        name=line[:line.find('\t')].replace(' ','').replace('?','').strip()
        if len(name)<=3:continue
        keywords=findkeywords(name)
        l=len(keywords)
        if (l==0) or (l==1):continue
        if (len(keywords[l-1])==1) and (keywords[l-1] not in deallist):
            print(name,' ',keywords)
            x=input('是否删除（y,n)?'+'\n')
            if x=='y':continue
        de1.write(line)
    f.close()
    de1.close()
