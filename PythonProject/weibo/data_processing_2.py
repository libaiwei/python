#coding=utf-8
i = 1
f = open('/Users/baiweili/Desktop/weibo/message_1.csv','r')
while True:
    try:
        if f.readline():
            line = f.readline()
            #长度大于10个字
            if len(line) > 50:
                print line
                path = '/Users/baiweili/Desktop/weibo/data/data2'+str(i)
                with open(path,'w') as f1:
                    f1.write(line)
                    f1.close()
                    i += 1
        else:
            break
    except:
        continue