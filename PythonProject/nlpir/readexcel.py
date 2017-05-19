# coding:gb18030
import xlrd
data = xlrd.open_workbook('/Users/baiweili/Desktop/a.xlsx')
f = open('/Users/baiweili/Desktop/zyj.txt','w')
table = data.sheets()[0]
nrows = table.nrows
for i in range(3,nrows,8):
    row = table.row_values(i)
    s = str(i+1)+','
    for r in row:
        if r != '':
            try:
                r = str(r)
            except:
                r
            r = r.strip()
            s += r+','
    f.write(s.strip(',').encode('gb18030')+'\n')