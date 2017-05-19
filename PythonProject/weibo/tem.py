
f = open('/Users/baiweili/Desktop/weibo/hour')
lines = f.readlines()
f.close()
d = {}
for l in lines:
    if l.startswith('2012-01-'):
        s = str(l)
        try:
            d[l] += 1
        except:
            d[l] = 1
for key,value in d.items():
    print key.strip()+','+str(value)
