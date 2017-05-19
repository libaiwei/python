# -*- coding:utf-8 -*-
__author__ = 'baiweili'

import urllib2
import re

def getMovieURL():
    url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    pattern = re.compile('<a href="(/title/.*?)"',re.S)
    items = re.findall(pattern,res)
    list = []
    i = 0
    for item in items:
        if i%2 == 0:
            item = 'http://www.imdb.com'+item
            list.append(item)
        i += 1

    return list
# if __name__ == '__main__':
#     getMovieURL()
    # return list