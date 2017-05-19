#coding:utf8
fin = open('/Users/baiweili/Downloads/A-large-practice.in','r')
fout = open('A-large-practice.out','w')
N = int(fin.readline())    #N test cases
for case in xrange(1, N + 1):
    C = int(fin.readline())
    l = int(fin.readline())#the number of items in the store
    P = map(int, fin.readline().strip().split()) #the price of each item
    max = 0
    for i in xrange(l):       #依次搜索
        for j in xrange(i + 1, l):
            sum = P[i] + P[j]
            if sum > max and sum <= C: #找到最大且小于C时，更新最大值和两个商品的号码
                max = sum
                best = [i,j]
    fout.write("Case #%d: %d %d \n" %(case, best[0] + 1, best[1] + 1))
    #print("Case #%d: %d %d \n" %(case, best[0] + 1, best[1] + 1))

fin.close()
fout.close()