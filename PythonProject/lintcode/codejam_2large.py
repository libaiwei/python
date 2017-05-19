# coding:utf8
fin = open('/Users/baiweili/Desktop/B-large.in','r')
fout = open('/Users/baiweili/Desktop/b.txt','w')
N = int(fin.readline())
for case in range(1, N + 1):
    flag = 0
    step = 0
    s = fin.readline().strip()
    if s:
        l = list(s)
        for i in range(len(l)-1):
            if int(l[i]) > int(l[i+1]):
                l[step] = str(int(l[step])-1)
                if int(l[0]) == 0:
                    result = ''.join(l[1:step+1]) + '9'*(len(l)-step-1)
                else:
                    result = ''.join(l[:step+1]) + '9'*(len(l)-step-1)
                flag = 1
                fout.write("Case #%d: %s \n" %(case, result))
                break
            elif int(l[i]) < int(l[i+1]):
                step = i+1
        if flag == 0:
            fout.write("Case #%d: %s \n" %(case, s))
fin.close()
fout.close()