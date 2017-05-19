# -*- coding:utf-8 -*-

import urllib2
import re
import requests

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
if __name__ == '__main__':
    #https://movie.douban.com/subject/26583812/ 没有简介
    # list = getMovieURL(200,52)
    f = open('/Users/baiweili/movie_table2')
    i = 1
    for l in f.readlines():
        l = l.strip()
        url = 'https://movie.douban.com/subject/'+str(l)
        if l:
            i+=1
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
                   "Accept-Language":'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   "Accept-Encodeing":"gzip, deflate, br"}
            r = requests.get(url,headers=headers)
            page = r.text
            pattern = re.compile('<span property="v:summary" class="">([\n\s\S\d\D\w\W]*?)</span>')
            match = re.findall(pattern,page)
            try:
                for m in match:
                    s = match[0].encode('gbk')
                    path = '/Users/baiweili/Desktop/movie/'+str(l)
                    print str(l)
                    f = open(path,'wb')
                    f.write(s)
            except:
                continue
    # k = 1
    # for l in list:
    #     print k,l
    #     # time.sleep(5)
    #     headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
    #                "Accept-Language":'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #                "Accept-Encodeing":"gzip, deflate, br"}
    #     r = requests.get(l,headers=headers)
    #     page = r.text
    #     pattern = re.compile('<span property="v:summary" class="">([\n\s\S\d\D\w\W]*?)</br>')
    #     match = re.findall(pattern,page)
    #     try:
    #         for m in match:
    #             s = match[0].encode('gbk')
    #             path = '/Users/baiweili/Desktop/movie/movie_'+str(k)
    #             f = open(path,'wb')
    #             f.write(s)
    #             k += 1
    #     except:
    #         continue
