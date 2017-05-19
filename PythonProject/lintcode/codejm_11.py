# coding:utf8
fin = open('/Users/baiweili/Desktop/A-large.in','r')
fout = open('A-large-practice.out','w')
N = int(fin.readline())    #N test cases
countlist = []
for case in xrange(1, N + 1):
    flag = 0
    count = 0
    l = fin.readline().strip().split()
    s = l[0]
    length = len(l[0])
    step = int(l[1])
    s1 = []
    count = 0
    for i in range(length):
        if s[i] is '-':
            s1.append(-1)
        else:
            s1.append(1)
    for i1 in range(length):
        if s1[i1] == -1:
            if i1+step <= length:
                for j in range(step):
                    s1[i1+j] *= -1
                count += 1
            else:
                flag = 1
                break
    if flag == 1:
        fout.write("Case #%d: %s \n" %(case, 'IMPOSSIBLE'))
    else:
        fout.write("Case #%d: %d \n" %(case, count))
fin.close()
fout.close()