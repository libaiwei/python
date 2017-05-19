# coding:utf8
fin = open('/Users/baiweili/Desktop/A-small-attempt0.in','r')
fout = open('A-small-practice.out','w')
N = int(fin.readline())
l = fin.readline()
while l:
    l = l.strip().split()
    row = int(l[0])
    col = int(l[1])
    rowlist = []
    for r in range(row):
        s = fin.readline().strip()
        ls = list(s)
        flag = 0
        for j in range(len(ls)):
            print ls
            if ls[j] is not '?':
                label = ls[j]
                flag = 1
            else:
                if flag == 1:
                    ls[j] = label
        for k1 in range(len(ls)):
            k = len(ls)-1-k1
            if ls[k] is not '?':
                label = ls[k]
                flag = 1
            else:
                if flag == 1:
                    ls[k] = label
        ls = ls.reverse()
        rowlist.append(ls)
    print rowlist
    l = fin.readline()
