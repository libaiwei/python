# -*- coding:utf-8 -*-
import urllib2
import re
import getMovieUrl

class DouBan:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0"
        self.headers = {
            'User-Agent': user_agent
        }
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
        for line in info.split('\n'):
            str_split = ''
            if line:
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
        pattern_2 = re.compile('<a href="(.*?)" rel="v:directedBy">(.*?)</a>')
        dirPath = re.findall(pattern_2,info)
        dirnamelist = []
        dirUrllist = []
        for s in dirPath:
            dirnamelist.append(s[1])
            dirUrllist.append('https://movie.douban.com'+s[0])
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


    def start(self,url):
        try:
            #get movie information
            pageCode = self.getPage(url)
            movie = self.gettitle(pageCode)
            year = self.getyear(pageCode)
            info = self.getInfo(pageCode)
            sortedInfo = self.getSortedInfo(movie,year,info)
            str = "','".join(sortedInfo)

            #get director information
            (dirnamelist,dirurllist) = self.getDirUrl(info)
            dirresultlist = []
            for (dnlist,dulist) in zip(dirnamelist,dirurllist):
                dirpageCode = self.getDirPage(dulist)
                dirinfo = self.getDirInfo(dirpageCode)
                dirSortedInfo = self.getDirSortedInfo(dirinfo)
                dirresultlist.append(dnlist + ' ' + dirSortedInfo)
                # print dirresult
                # datalist = sortedInfo.extend(dirSortedInfo)
            dirresult = ' | '.join(dirresultlist)
            result = 'insert into Movie_info values(' + "'" + str + "','" + dirresult + "')"
            return result

            # print self.gettitle(pageCode)
            # for l in sortedInfo:
                # print l
        except Exception,e:
            print Exception,":",e

# pattern_1 = re.compile()