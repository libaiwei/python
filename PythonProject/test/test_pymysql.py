__author__ = 'baiweili'
import pymysql
conn = pymysql.connect(host='127.0.0.1',user='root',passwd='lbw')
cur = conn.cursor()
cur.execute('use douban')
cur.execute('select * from IMDB_done WHERE RANK=5')
print(cur.fetchone())
cur.close()
conn.close()