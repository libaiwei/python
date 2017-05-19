__author__='libaiwei'
#coding=utf-8

import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({'username':'woshilibaiwei','password':'woshilibaiwie'})
loginurl = 'https://auth.bupt.edu.cn/authserver/login?service=http%3a%2f%2fwelcome.bupt.edu.cn%2findex.portal'
cookie.save(ignore_expires=True,ignore_discard=True)
gradeUrl='http://welcome.bupt.edu.cn/index.portal?.pn=p21545'
result = opener.open(gradeUrl)
print result.read()