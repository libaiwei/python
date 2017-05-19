# coding:utf8
# from ctypes import c_longlong as longlong
fin = open('/Users/baiweili/Desktop/B-small-attempt0.in','r')
fout = open('/Users/baiweili/Desktop/b.txt','w')
N = int(fin.readline())
for case in xrange(1, N + 1):
    s = fin.readline().strip()
    if s:
        s = int(s)
        for s in range(s,0,-1):
            flag = 0
            s_str = str(s)
            for i in range(len(s_str)-1):
                if s_str[i] > s_str[i+1]:
                    flag = 1
                    break
            if flag == 0:
                fout.write("Case #%d: %d \n" %(case, s))
                break

