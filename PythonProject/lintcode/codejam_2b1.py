# coding:utf8
fin = open('/Users/baiweili/Desktop/A-large-practice (1).in','r')
fout = open('/Users/baiweili/Desktop/b.txt','w')
N = int(fin.readline())
for i in range(N):
    l2 = fin.readline()
    target = float(l2.strip().split()[0])
    horse_num = int(l2.strip().split()[1])
    r = []
    for j in range(horse_num):
        h = fin.readline()
        location = float(h.split()[0])
        speed = float(h.split()[1])
        time = (target-location)/speed
        rs = target/time
        r.append(rs)
    result = min(r)
    print result
    fout.write("Case #%d: %s \n" %(i+1, result))
fin.close()
fout.close()
