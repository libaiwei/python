# coding:utf8
fin = open('/Users/baiweili/Desktop/B-small-practice.in','r')
fout = open('/Users/baiweili/Desktop/b.txt','w')
N = int(fin.readline())
for i in range(N):
    l2 = fin.readline()
    num = int(l2.strip().split()[0])
    d = {}
    d['R'] = int(l2.strip().split()[1])
    d['O'] = int(l2.strip().split()[2])
    d['Y'] = int(l2.strip().split()[3])
    d['G'] = int(l2.strip().split()[4])
    d['B'] = int(l2.strip().split()[5])
    d['V'] = int(l2.strip().split()[6])
    str = ''
    for k,v in d.items():
        if v != 0:
            str += v*k
    from itertools import permutations
    print list(permutations(str))
fin.close()
fout.close()

