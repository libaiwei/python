# -*- coding:utf-8 -*-
import urllib2
import re
import getMovieUrl
import mysql.connector

class IMDB:


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
    def getMovie(self,pageCode):
        pattern = re.compile('<h1 itemprop="name".*?>(.*?)&nbsp')
        match = re.search(pattern,pageCode)
        movie = match.group(1)
        return movie
    def getYear(self,pageCode):
        pattern = re.compile('<a href="/year/(.*?)/')
        match = re.search(pattern,pageCode)
        year = match.group(1)
        return year


    def getDirInfo(self,pageCode):
        pattern = re.compile('<span itemprop="director"[\n\s\S\d\D\w\W]*?<a href="(.*?)"[\n\s\S\d\D\w\W]*?itemprop="name">(.*?)</span>',re.S)
        # items = re.findall(pattern,pageCode)
        # for item in items:
        #     dirInfo = item[1]
        #     dirUrl = item[0]
        match = re.search(pattern,pageCode)
        dirUrl = match.group(1)
        dirInfo = match.group(2)
        return dirUrl,dirInfo
    def getWriter(self,pageCode):
        pattern = re.compile('<h4 class="inline">Writer[s]?:</h4>[\n\s\S\d\D\w\W]*?<span itemprop="creator"[\n\s\S\d\D\w\W]*?</span>[\n\s\S\d\D\w\W]*?</div>')
        match = re.findall(pattern,pageCode)
        sortedCode = ''.join(match)
        pattern_1 = re.compile('<span class="itemprop" itemprop="name">(.*?)</span>',re.S)
        items = re.findall(pattern_1,sortedCode)
        writer = ','.join(items)
        return writer
    def getStars(self,pageCode):
        pattern = re.compile('<h4 class="inline">Stars:</h4>[\n\s\S\d\D\w\W]*?<span itemprop="actors"[\n\s\S\d\D\w\W]*?</span>[\n\s\S\d\D\w\W]*?</div>')
        match = re.findall(pattern,pageCode)
        sortedCode = ''.join(match)
        pattern_1 = re.compile('<span class="itemprop" itemprop="name">(.*?)</span>',re.S)
        items = re.findall(pattern_1,sortedCode)
        stars = ','.join(items)
        return stars
    def getBornInfo(self,dirPage):
        pattern = re.compile('<div id="name-born-info" class="txt-block">[\n\s\S\d\D\w\W]*?</div>',re.S)
        match = re.search(pattern,dirPage)
        bornInfo = match.group(0)
        return bornInfo
    def getbirthDate(self,bornInfo):
        pattern = re.compile('<time datetime="(.*?)" itemprop="birthDate">',re.S)
        match = re.search(pattern,bornInfo)
        birthDate = match.group(1)
        return birthDate
    def getbirthPlace(self,bornInfo):
        pattern = re.compile('birth_place=.*?>(.*?)<',re.S)
        match = re.search(pattern,bornInfo)
        birthPlace = match.group(1)
        return birthPlace

    def start(self):
        conn = mysql.connector.connect(
        user='root',
        password='lbw',
        host='localhost',
        database='douban')
        cursor = conn.cursor()
        try:
            #get movie information
            urllist = getMovieUrl.getMovieURL()
            rank = 1
            for url in urllist:
                pageCode = self.getPage(url)
                (dirUrl,director) = self.getDirInfo(pageCode)
                dirUrl = 'http://www.imdb.com'+dirUrl
                dirPage = self.getPage(dirUrl)
                try:
                    bornInfo = self.getBornInfo(dirPage)
                    birthDate = self.getbirthDate(bornInfo)
                    birthPlace = self.getbirthPlace(bornInfo)
                except:
                    birthDate = ''
                    birthPlace = ''

                movie = self.getMovie(pageCode)
                year = self.getYear(pageCode)

                writer = self.getWriter(pageCode)
                stars = self.getStars(pageCode)
                value = '('+str(rank)+',"'+movie+'","'+year+'","'+director+'","'+writer+'","'+stars+'","'+birthDate+'","'+birthPlace+'")'
                print 'Rank',rank,value
                sql = 'insert into IMDB values'+value
                # cursor.execute(sql)
                rank += 1
                print movie
                print year
                print director
                print writer
                print stars
                print birthDate
                print birthPlace
        except Exception,e:
            print Exception,":",e
        conn.close()
spider = IMDB()
spider.start()