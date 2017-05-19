# -*- coding:utf-8 -*-
f = open('/Users/baiweili/Desktop/del1','r')
f1=open('/Users/baiweili/Desktop/del2','w')
str = ''
while True:
    line = f.readline()
    s = ''.join(line.split())
    if line:
        str += 'insert into del values("' + s + '");'
    else:
        break
f1.write(str)
f.close()
