#coding:utf-8
import os
import os.path
def bays(words_ceshi_list):
    count = 0
    result = 'XXX'
    for root,dirs,files in os.walk('/Users/baiweili/Desktop/result'):
        for file in files:
            if not file.__contains__('.DS_Store'):
                path = os.path.join(root,file)
                f = open(path)
                words_list = []
                num = 0
                while True:
                    l = f.readline()
                    if l:
                        words = l.split()
                        if words[0] in words_ceshi_list:
                            num += 1
                        # words_list.append(words[0])
                    else:
                        break
                # list = list(set(words_ceshi_list).intersection(set(words_list)))
                if num>count:
                    count = num
                    result = file
    return result
def ceshi(file):
    path = os.path.join(root,file)
    f = open(path)
    words_ceshi_list = []
    while True:
        l = f.readline()
        if l:
            words = l.split()
            words_ceshi_list.append(words[0])
        else:
            break
    return words_ceshi_list
if __name__ == '__main__':
    i = 11
    for root,dirs,files in os.walk('/Users/baiweili/Desktop/output_zsq'):
        right = 0
        wrong = 0
        if not root is '/Users/baiweili/Desktop/output_zsq':
            name = root.split('/')
            name = name[-1]
            for root,dirs,files in os.walk(root):
                for file in files:
                    if not file.__contains__('.DS_Store'):
                        words_ceshi_list = ceshi(file)
                        result = bays(words_ceshi_list)
                        # print name,result
                        if result == name:
                            right+=1
                        else:
                            wrong+=1
                        # print result
            right=i*right
            wrong=i*wrong
            print name
            print 'right =',right
            print 'wrong =',wrong
            print float(right)/float(right+wrong)