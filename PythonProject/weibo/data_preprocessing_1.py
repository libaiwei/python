#coding=utf-8
import csv

ulist = []
mlist = []
ucheck = {}

with open('/Users/baiweili/Desktop/weibo/test2.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        ulist.append(row[0])
        mlist.append(row[1])
    ulist = ulist[1:]
    mlist = mlist[1:]
k = 0
for u in ulist:
    if not ucheck.has_key(u):
        ucheck[u] = mlist[k]
    else:
        ucheck[u] = ucheck[u] + '\n' +mlist[k]
    k += 1
for key,value in ucheck.items():
    print key,value
    path = '/Users/baiweili/Desktop/weibo/data/'+key
    with open(path,'w') as f:
        f.write(value)
        f.close()