# coding:utf8
import math
# def sortedDict(adict):
#     keys = adict.keys()
#     keys.sort()
#     return [dict[key] for key in keys]
fin = open('/Users/baiweili/Desktop/a.txt','r')
fout = open('/Users/baiweili/Desktop/b.txt','w')
N = int(fin.readline())
for i in range(N):
    l2 = fin.readline()
    cakenum = int(l2.strip().split()[0])
    j = int(l2.strip().split()[1])
    caker = {}
    cakeh = []
    cakes = []
    for i in range(cakenum):
        l3 = fin.readline()
        r = float(l3.strip().split()[0])
        h = float(l3.strip().split()[1])

        if caker.has_key(r):
            caker[r].append(h)
            caker[r] = sorted(caker[r])
        else:
            caker[r] = [h]
        # s = math.pi * r * r
        # cakes.append(s)
    caker = [(k,caker[k]) for k in sorted(caker.keys())]
    caker1 = {}
    # for i in range(cakenum):
    #     caker1[i] = caker
    # print(caker)
    # print caker
    # cakes.append(0.0)
    # cakes = sorted(caker.i)
    result = []
    s0 = 0.0
    for r,H in caker:
        for h in H:
            s1 = math.pi * r * r
            s = s1 - s0 + 2.0*math.pi*r*h
            result.append([s,s0])
            s0 = s1

    result = sorted(result,reverse=True)
    r3 = []
    print result
    # result = result[:len(result)-j-1:-1]
    s = 0
    for m in result[:j]:
        s += m[0]
    s += result[j-1][1]

    print s


