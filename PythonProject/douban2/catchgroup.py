import requests
import re
from bs4 import BeautifulSoup
import pickle
import time
def load_cookie():
    with open('cookies.txt', 'rb') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    return cookies
def pattern(l):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
               "Accept-Language":'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               "Accept-Encodeing":"gzip, deflate, br"}
    url = 'https://www.douban.com/group/people/'+str(l) + '/joins'
    rs = requests.Session()
    # rs.cookies = cookies
    # r = rs.get(url, cookies=rs.cookies, headers=headers)
    r=rs.get(url,headers=headers)
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    result = soup.findAll('div', attrs={"class": "info"})
    p = re.compile('https://www.douban.com/group/(.*?)/')
    group = []
    for l in result:
        try:
            l = re.search(p,str(l)).group(1)
        except:
            continue
        group.append(l)
    return group
# cookies = load_cookie()
file = '/Users/baiweili/Desktop/per'
f = open(file,'r')
lines = f.readlines()
f.close()
s = ''
for l in lines:
    l = l.strip()
    try:
        group = pattern(l)
    except:
        continue
    for g in group:
        g = str(l) + ' ' + str(g) + '\n'
        print g
        sfile = '/Users/baiweili/Desktop/sfile'
        f1 = open(sfile,'a+')
        f1.write(g)
        f1.close()
    time.sleep(3)
# sfile = '/Users/baiweili/Desktop/sfile'
# f1 = open(sfile,'a+')
# f1.write(s)
# f1.close()
# print len(pattern('19619577'))

# url = 'https://www.douban.com/group/people/19619577/joins'
# r = rs.get(url, cookies=rs.cookies, headers=headers)
# page = r.text
# soup = BeautifulSoup(page, "html.parser")
# result = soup.findAll('div', attrs={"class": "article"})
# divtext = '<div class="group-list group-cards">'
# pattern = re.compile('href=\"https://www.douban.com/group/(.*?)/')
# items = re.findall(pattern,res)
# list = []
# for item in items:
#     s = item
#     list.append(s)
# print list

