# -*- encoding:utf-8 -*-
##############################
__author__ = "LiBaiwei"
__date__ = "2016/10/06"
###############################

import requests
from bs4 import BeautifulSoup
import urllib
import re
import time
import pickle
import os
import cookielib
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

        # if k==1:
        #     # '''''获取验证码图片'''
        #     #利用bs4获取captcha地址
        #     soup = BeautifulSoup(page,"html.parser")
        #     captchaAddr = soup.find('img',id='captcha_image')['src']
        #     #利用正则表达式获取captcha的ID
        #     reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        #     captchaID = re.findall(reCaptchaID,page)
        #     #print captchaID
        #     #保存到本地
        #     urllib.urlretrieve(captchaAddr,"captcha.jpg")
        #     captcha = raw_input('please input the captcha:')
        #
        #     formData['captcha-solution'] = captcha
        #     formData['captcha-id'] = captchaID
        #     r = self.rs.post(loginUrl,data=formData,headers=self.headers)
        #     page = r.text
        # return page

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
                print l,'qq'
                movies = self.get_Movie(l)
                for movie in movies:
                    print person,l,movie
                people.append(l)
        return people
    def save_cookie(self):
        with open(self._cookies_file, 'wb') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.rs.cookies), f)
            print(self.rs.cookies)

    def load_cookie(self):
        with open(self._cookies_file, 'rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            self.rs.cookies = cookies
    def get_list(people,self):
        list = []
        for person in people:
            time.sleep(3)
            list = list + self.pattern(person)
        return list
    def get_Movie(self,person):
        url = 'https://movie.douban.com/people/' + person + '/collect'
        r = self.rs.post(url, cookies=self.rs.cookies, headers=self.headers)
        page = r.text
        soup = BeautifulSoup(page,"html.parser")
        result = soup.findAll('li',attrs={"class":"title"})
        pattern = re.compile('https://movie.douban.com/subject/(.*?)/')
        movies = []
        for item in result:
            match = re.search(pattern,str(item))
            name = item.find('a').get_text()
            result = match.group(1) + ' ' + name
            movies.append(result)
        return movies
    def start(self):
        person_1 = 'beattywell'
        k = 1
        self.send_message(person_1,k)
        people = self.pattern(person_1)
        for person in people:
            self.pattern(person)
        # for i in range(1,10):
        #     people = self.get_list(people)
        # self.get_list(people)
        # if os.path.exists(self._cookies_file):
        #     self.load_cookie()
        # else:
        #     self.save_cookie()
spider = spider()
spider.start()