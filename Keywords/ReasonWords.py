__author__ = 'Han'
import jieba

if __name__=='__main__':
    f=open('D:\\Unit0922.txt','r')
    fw=open('D:\\Reason.txt','w')
    wordcount={}
    classlist=['借款','贷款','医疗费','违约金','工资','工程款','赔偿款','租金','保证金','定金','合同','None']
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
            if '借款' in wordlist:wordcount['借款']+=1
            elif '贷款' in wordlist:wordcount['贷款']+=1
            elif '租金' in wordlist:wordcount['租金']+=1
            elif '工程款' in wordlist:wordcount['工程款']+=1
            elif '医疗费' in wordlist:wordcount['医疗费']+=1
            elif '保证金' in wordlist:wordcount['保证金']+=1
            elif '工资' in wordlist:wordcount['工资']+=1
            elif '定金' in wordlist:wordcount['定金']+=1
            elif '合同' in wordlist:wordcount['合同']+=1
            elif '违约金' in wordlist:wordcount['违约金']+=1
            else:
                print(reason)
                print(wordlist)
                try:
                    cla=input('名目:'+'\n')
                    cla=int(cla)
                except Exception:
                    wordcount[cla]+=1
                else:
                    wordcount[wordlist[cla]]+=1
        else:
            wordcount['None']+=1
            fw.write(reason+'\n')
    wordcount=sorted(wordcount.items(),key=lambda d:d[1],reverse=True)
    print(wordcount)