# -*- encoding:utf-8 -*-
##############################
__author__ = "LiBaiwei"
__date__ = "2016/10/06"
###############################

import requests
from bs4 import BeautifulSoup
import re
import time
import pickle
class spider:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
                   "Accept-Language":'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   "Accept-Encodeing":"gzip, deflate, br"}
        self.rs = requests.Session()
        self._cookies_file = 'cookies.txt'
    def send_message(self, person, k):
        url = 'https://www.douban.com/people/' + person + '/rev_contacts'
        loginUrl = 'https://accounts.douban.com/login'
        formData={
            "redir":url,
            "form_email":'775891727@qq.com',
            "form_password":'qwe123456789',
            "login":u'登录'
        }

        r = self.rs.post(loginUrl, data=formData, headers=self.headers)
        page = r.text

    def pattern(self, person):
        url = 'https://www.douban.com/people/' + str(person) + '/rev_contacts'
        r = self.rs.get(url, cookies=self.rs.cookies, headers=self.headers)
        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        result = soup.findAll('div', attrs={"class": "article"})
        pattern = re.compile('https://www.douban.com/people/(.*?)/')
        #print result
        people = []
        for item in result:
            list = item.findAll('dd')
            for l in list:
                l = re.search(pattern,str(l)).group(1)
                print 'insert into per_table values("' + person + '","' + l + '");'
                people.append(l)
        return people
    def get_Movie(self,person):
        url = 'https://movie.douban.com/people/' + person + '/collect'
        r = self.rs.post(url, cookies=self.rs.cookies, headers=self.headers)
        page = r.text
        soup = BeautifulSoup(page,"html.parser")
        films = soup.findAll('div',attrs={"class":"info"})
        names = soup.findAll('li',attrs={"class":"title"})
        infos = soup.findAll('li',attrs={"class":"intro"})
        pattern = re.compile('https://movie.douban.com/subject/(.*?)/')
        movies = []
        # for name in names:
        #     match = re.search(pattern_1,str(name))
        #     print match.group(1)
        for (name,info,f) in zip(names,infos,films):
            match = re.search(pattern,str(name))
            name = name.find('a').get_text()
            name = ''.join(name.split())
            result = match.group(1) + ' ' + name
            score = f.find(name='span',attrs={'class':re.compile(r'rating\d-t')})
            score = str(score)[19:20]
            sql = 'insert into movie_table values("' + person + '","' + match.group(1) + '","' + name + '","' + score + '","' + info.get_text() + '");'
            sql = sql.encode('utf-8').strip()
            print sql
        #     movies.append(result)
        # return movies
    def load_cookie(self):
        with open(self._cookies_file, 'rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            self.rs.cookies = cookies
    def getlist(self,list):
        list_1 = []
        for l in list:
            time.sleep(3)
            list_1 += self.pattern(l)
        return list_1
    def digui(self,N,startlist):
        if N == 0 or N == 1:
            return startlist
        else:
            return self.getlist(self.digui(N-1,startlist))
    def start(self):
        f = open('name')
        while 1:
            person = f.readline()
            if person:
                self.get_Movie(''.join(person.split()))
                time.sleep(3)
            else:
                break

        # print type(people)
        # for person in people:
        #     self.get_Movie(str(person))
        #     time.sleep(3)
spider = spider()
spider.start()