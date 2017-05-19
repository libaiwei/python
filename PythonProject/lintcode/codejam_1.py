fin = open('/Users/baiweili/Desktop/A-small-attempt0.in','r')
fout = open('A-small-practice.out','w')
N = int(fin.readline())    #N test cases
l1 = []
for case in xrange(1, N + 1):
    l = fin.readline().strip().split()
    step = int(l[1])
    # lo = len(l[0])
    str1 = l[0]
    if len(str1)-step<step:
        union = str1[len(str1)-step:step]
        if union.__contains__('+') and union.__contains__('-'):
            fout.write("Case #%d: %s \n" %(case, 'IMPOSSIBLE'))
        else:
            s = l[0].split('+')
            s1 = []
            for i in range(len(s)):
                s[i] = len(s[i])
                if s[i] != 0:
                    if s[i]%step == 0:
                        s1.append(s[i]/step)
                    else:
                        s1.append(s[i]/step+1)
            fout.write("Case #%d: %d \n" %(case, len(s1)))
    else:
        s = l[0].split('+')
        s1 = []
        for i in range(len(s)):
            s[i] = len(s[i])
            if s[i] != 0:
                if s[i]%step == 0:
                    s1.append(s[i]/step)
                else:
                    s1.append(s[i]/step+1)
        fout.write("Case #%d: %d \n" %(case, len(s1)))
fin.close()
fout.close()