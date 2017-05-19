# -*- coding:utf-8 -*-
import urllib2
import re
import getMovieUrl
import mysql.connector
import login
import requests
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
class DouBan:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0"
        self.headers = {
            'User-Agent': user_agent
        }
        self.rs = requests.Session()
        self._cookies_file = 'cookies.txt'
    def getPage(self,url):
        try:
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            # print pageCode
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        return pageCode
    def getInfo(self,pageCode):
        pattern = re.compile('<div id="info">(.*?)</div>',re.S)
        items = re.findall(pattern,pageCode)
        info = ''
        for item in items:
            info += item
        return info
    def getSortedInfo(self,movie,year,info):
        list = [movie,year]
        pattern_1 = re.compile('>(.*?)<')
        pattern_2 = re.compile('/celebrity/(\d+/)')
        for line in info.split('\n'):
            str_split = ''
            if 'celebrity' in line:
                line_split = re.findall(pattern_2,line)
                for l in line_split:
                    str_split += l
                list.append(str_split)
            elif line:
                line_split = re.findall(pattern_1,line)
                for l in line_split:
                    str_split += l
                list.append(str_split)
        return list

    def gettitle(self,pageCode):
        pattern = re.compile('<span property="v:itemreviewed">(.*?)</span>',re.S)
        items = re.findall(pattern,pageCode)
        movie = ''
        for item in items:
            movie += item
        return movie
    def getyear(self,pageCode):
        pattern = re.compile('<span class="year">(.*?)</span>',re.S)
        items = re.findall(pattern,pageCode)
        year = ''
        for item in items:
            year += item
        return year

    #get director information
    def getDirUrl(self,info):
        pattern_2 = re.compile('<a href="(.*?)/" rel="v:directedBy">')
        dirPath = re.findall(pattern_2,info)
        dirnamelist = []
        dirUrllist = []
        for s in dirPath:
            dirnamelist.append(s)
            dirUrllist.append('https://movie.douban.com'+s)
        return dirnamelist,dirUrllist
    def getDirPage(self,dirUrl):
        try:
            request = urllib2.Request(dirUrl,headers = self.headers)
            response = urllib2.urlopen(request)
            dirpageCode = response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        return dirpageCode
    def getDirInfo(self,dirpageCode):
        pattern = re.compile('<div class="info">(.*?)</div>',re.S)
        items = re.search(pattern,dirpageCode)
        dirinfo = ''
        if items:
            dirinfo = items.group(0)
        else:
            print 'Not match'
        return dirinfo
    def getDirSortedInfo(self,dirinfo):
        pattern = re.compile('>([\n\s\S\d\D\w\W]*?)<')
        match = re.findall(pattern,dirinfo)
        dirSortedInfo = ''
        for m in match:
            dirSortedInfo = dirSortedInfo+m
        dirSortedInfo = ' '.join(dirSortedInfo.split())
        return dirSortedInfo
##<div class="comment-item" data-cid="1011305534">
    def getCommentpage(self,i,url):
        url1 = url + 'comments?start=' + str(i) + '&limit=20&sort=new_score'
        # try:
        #     request = urllib2.Request(url,headers = headers)
        #     response = urllib2.urlopen(request)
        #     pageCode = response.read().decode('utf-8')
        #     return pageCode
        #     # print pageCode
        # except urllib2.URLError, e:
        #     if hasattr(e, "code"):
        #         print e.code
        #     if hasattr(e, "reason"):
        #         print e.reason
        formData={
        "redir":url1,
        "form_email":'775891727@qq.com',
        "form_password":'qwe123456789',
        "login":u'登录'
        }
        r = requests.post(url1,data=formData,headers=self.headers)
        page = r.text
        return page

    def getCommentInfo(self,pageCode):
        # pattern = re.compile('<span class="comment-info">[\n\s\S\d\D\w\W]*?<a href="https://www.douban.com/people/(.*?)/[\n\s\S\d\D\w\W]*?title="(.*?)"[\n\s\S\d\D\w\W]*?(\d+-\d+-\d+)')
        #贪婪模式('.'匹配字符,包括换行符)re.findall(r"AAA(.*)CCC",pageCode,re.S)

        items = re.findall('<span class="comment-info">[ \t\n\r\f]+<a href="https://www.douban.com/people/(.*?)/(.*?)</a>[ \t\n\r\f]+<span class="allstar\d+ rating" title="(.*?)"></span>[\n\s\S\d\D\w\W]*?(\d+-\d+-\d+)',pageCode)
        return items
        # return items
    def start(self):
        # conn = mysql.connector.connect(
        # user='root',
        # password='lbw',
        # host='localhost',
        # database='douban')
        # cursor = conn.cursor()
        urllist = getMovieUrl.getMovieURL(300,0)

        # login.login()

        try:
            #get movie information
            for url in urllist:
                time.sleep(3)
                try:
                    pageCode = self.getPage(url)
                except:
                    time.sleep(10)
                    print 'Sleep.....'
                    continue
                # pageCode = self.getPage(url)
                movie = self.gettitle(pageCode)
                year = self.getyear(pageCode)
                year = year[1:-1]
                info = self.getInfo(pageCode)
                sortedInfo = self.getSortedInfo(movie,year,info)
                if len(sortedInfo) == 15:
                    sortedInfo = sortedInfo[:-2]
                id = sortedInfo[-1]
                id = id.split(' ')[-1]

                str = "','".join(sortedInfo[:-1]) + "','" + id

                #get director information
                (dirnamelist,dirurllist) = self.getDirUrl(info)
                dirresultlist = []
                dnresultlist = []
                for (dnlist,dulist) in zip(dirnamelist,dirurllist):
                    dirpageCode = self.getDirPage(dulist)
                    dirinfo = self.getDirInfo(dirpageCode)
                    dirSortedInfo = self.getDirSortedInfo(dirinfo)
                    dnresultlist.append(dnlist)
                    dirresultlist.append(dirSortedInfo)
                    # print dirresult
                    # datalist = sortedInfo.extend(dirSortedInfo)
                dirresult = ' | '.join(dirresultlist)
                dnresult = ''.join(dnresultlist)
                result = 'insert into Movie_info values(' + "'" + str + "')"
                result1 = 'insert into DIR_info values(' + "'" + dnresult + "','" + id + "','"+ dirresult +"')"
                # cursor.execute(result)
                # cursor.execute(result1)
                print result
                print result1
                k = 0
                for i in range(0,50):
                    # if k == 101:
                    #     break
                    j = 20*i
                    CommentpageCode = self.getCommentpage(j,url)
                    time.sleep(2)
                    try:
                        int(CommentpageCode.count)
                    except:
                        k += 1
                        if k == 20:
                            break
                    comments = self.getCommentInfo(CommentpageCode)
                    for comment in comments:
                        # k += 1
                        # if k==101:
                        #     break
                        # print k
                        result2 = 'insert into Comment_Info values(' + "'" + id + "','" + comment[0] + "','" + comment[2] + "','"+ comment[3] +"')"
                        # cursor.execute(result2)
                        print result2
        except Exception,e:
            print Exception,":",e
spider = DouBan()
spider.start()