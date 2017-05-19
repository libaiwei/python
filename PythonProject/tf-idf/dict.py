#coding=utf-8
def dict(path):
    f = open(path,'r')
    lines=f.readlines()
    f.close()
    D = {}
    for line in lines:
        # line = unicode(line,'gbk').rstrip('\n')
        line = line.rstrip('\n')
        if line:
            words = line.split()
            print words
            D[words[0]] = words[1]
    return D