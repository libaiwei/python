f = open('/Users/baiweili/Desktop/tempdata1.txt','r')
f1 = open('per_1','w')
i = 0
while True:
    line = f.readline()
    if line:
        i += 1
        j = 1
        words = line.split(',')
        for word in words:
            word = ''.join(word.split())
            s = 'insert into head values(1,' + str(j) + ',' + str(i) + ',' + word + ');'
            f1.write(s)
            j += 1
    else:
        break
f.close()
