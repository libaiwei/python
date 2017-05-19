
def decide():
    s = '-1.0 0.0 1.0 1.0 1.0 -1.0 0.0 0.0'
    list = s.split()
    list1 = []
    list2 = []
    for i in range(len(list)):
        if i%2==0:
            list1.append(float(list[i]))
        else:
            list2.append(float(list[i]))
    x = list1[-1]
    y = list2[-1]
    j = len(list)-1
    for m in range(j):
        if x==list1[m] and y==list2[m]:
            print 'tr'
            # return True
        else:
            for n in range(m+1,j):
                a = y-list2[m]
                b = y-list1[m]
                if (y-list2[m])/(x-list1[m])==(y-list2[n])/(x-list1[n]) and a*b<0:
                    # return True
                    print 't'
                else:
                    # return False
                    print 'f'
decide()




