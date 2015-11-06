__author__ = 'Han'
import jieba

if __name__=='__main__':
    f=open('D:\\Unit0922.txt','r')
    wordcount={}
    classlist=['借款','贷款','医疗费','违约金','工资','工程款','赔偿款','租金','保证金','定金','None']
    for cla in classlist:wordcount[cla]=0
    for line in f.readlines():
        k1=line.find('\t')
        k2=line[k1+1:].find('\t')
        name=line[:k1]
        reason=line[k1+1:k1+k2]
        wordlist=[]
        for cla in classlist:
            if reason.find(cla)!=-1:wordlist.append(cla)
        if len(wordlist)==1:wordcount[wordlist[0]]+=1
        elif len(wordlist)>1:
            print(reason)
            print(wordlist)
            cla=int(input('名目:'+'\n'))
            if wordlist[cla] in wordcount:wordcount[wordlist[cla]]+=1
            else:wordcount[wordlist[cla]]=1
        else:
            wordcount['None']+=1
    wordcount=sorted(wordcount.items(),key=lambda d:d[1],reverse=True)
    print(wordcount)