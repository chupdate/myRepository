__author__ = 'Han'

if __name__=='__main__':
    classdict={'联系':'失联','未按':'未公示年报','未依照':'未公示年报','隐瞒':'年报弄虚作假','弄虚作假':'年报弄虚作假','未在':'未公示年报'}
    f=open("D:\\GSXT\\GSXT整理temp.txt",'r')
    fw=open('D:\\GSXT\\GSXT整理class.txt','w')
    for line in f.readlines():
        relist=line.split('|')
        name=relist[0]
        reason=relist[3]
        reasondict={}
        if reason:
            if reason in ['隶属主体列入经营异常名录','2014年度，隶属主体列入经营异常名录','2013年度，隶属主体列入经营异常名录']:
                reasondict['经营异常']=1
            else:
                for cla in classdict.keys():
                    if reason.find(cla)!=-1:reasondict[classdict[cla]]=1
                if len(reasondict)!=1:
                    print(reason)
                    rea=input('请输入类别：'+'\n')
                    reasondict[rea]=1
        else:
            reasondict['经营异常']=1
        clalist=[]
        for cla in reasondict.keys():clalist.append(cla)
        relist[3]=clalist[0]
        fw.write('|'.join(relist))
    f.close()
    fw.close()

