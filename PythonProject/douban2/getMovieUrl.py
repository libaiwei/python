# -*- coding:utf-8 -*-
__author__ = 'baiweili'

import urllib2
import re

def getMovieURL(num,start):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=rank&page_limit="+ str(num) + "&page_start=" + str(start)
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    pattern = re.compile('"url":"(.*?)"',re.S)
    items = re.findall(pattern,res)
    list = []
    for item in items:
        s = item.replace('\\','')
        list.append(s)
    return list