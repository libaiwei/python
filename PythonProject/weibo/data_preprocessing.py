file = '/Users/baiweili/Desktop/weibo/week1.csv'
file1 = '/Users/baiweili/Desktop/weibo/user.csv'
f = open(file,'r')
f1 = open(file1,'w')
k = 1
while True:
    try:
        if f.readline():
            line = f.readline()
            words = line.split(',')
            re_uid = words[3]
            if str(re_uid):
                s = words[2] + ',' + words[3]
                f1.write(s)
                f1.write('\n')
                print k,re_uid
                k += 1
        else:
            break
    except:
        continue
