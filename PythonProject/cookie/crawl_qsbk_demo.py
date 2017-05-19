# -*- coding:utf-8 -*-
import urllib2
import re
class QSBK:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0"
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accepr-Encoding': "gzip, deflate",
            'Cookie': '_xsrf=2|50f02133|b2c6b69ca82f2592391bf0146ceeae57|1471607387; _qqq_uuid_="2|1:0|10:1471607387|10:_qqq_uuid_|56:ZGExMGRkN2JmYTk4NWVmYTAxNzBhM2UwMDMyZmI4ZmRhYTcxY2UwOA==|eac221cf5fc38fde6668b7de88fccc49309aa64d253120ab02ecb064dbd6d31f"; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1471607391; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1471607447; _ga=GA1.2.2105719701.1471607392; _gat=1',
            'Connection': "keep-alive",
            'Host': "www.qiushibaike.com",
            'User-Agent': user_agent,
            'Upgrade-Insecure-Request': "1"
        }

    def get_page(self,page_Index):
        url = "http://www.qiushibaike.com/hot/"+str(page_Index)
        try:
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode.strip()
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
    def get_items(self,pageCode):
        pattern = re.compile('(<a href=.*?target="_blank" title="(.*?)">)|(<div class="content">([\n\s\S\d\D\w\W]*?)</div>)|(<span class="stats-vote"><i class="number">(.*?)</i>(.*?)</span>)|(<i class="number">(.*?)</i>)',re.S)
        items = re.findall(pattern,pageCode)
        for item in items:
            print item[1],item[3],item[5],item[6],item[8]
            # print item
    def start(self):
        try:
            pageIndex = input("Enter a page number:")
            pageCode = self.get_page(pageIndex)
            self.get_items(pageCode)

        except Exception,e:
            print Exception,":",e
spider = QSBK()
spider.start()