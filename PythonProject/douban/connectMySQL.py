# -*- coding:utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='lbw',
         host='localhost',
         database='douban')
cursor = conn.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS Movie_info")

# 创建数据表SQL语句
sql = """CREATE TABLE Movie_info (
         MOVIE  CHAR(40) NOT NULL,
         YEAR CHAR(20),
         DIRECTOR  CHAR(40),
         SCRIPTWRITER CHAR(100),
         ROLE CHAR(100),
         TYPE CHAR(20),
         SITE CHAR(40),
         COUNTRY CHAR(20),
         LANGUAGE CHAR(20),
         DATE CHAR(20),
         LENGTH CHAR(20),
         ALTNAME CHAR(40),
         IMDB CHAR(20),
         DIRInfo CHAR(100))"""
cursor.execute(sql)
# values =      # 列表对象，dir()函数可以查看列表可以的操作
# 生成参数值


# sql = "insert into Movie_info values(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
# cursor.execute(sql)
# 关闭数据库


# sql = "insert into Movie_info values('海蒂和爷爷 Heidi','(2015)','导演: 阿兰·葛斯彭纳','编剧: Johanna Spyri / Petra Biondina Volpe','主演: 阿努克·斯特芬 / 安娜·申斯 / 莉莲·奈福 / 布鲁诺·甘茨 / 克里斯托夫·高格勒 / 昆林·艾格匹 / 丽贝卡·因德穆 / 莫妮卡·古布瑟 / 阿瑟·比勒 / 彼得·罗美尔 / 卡塔琳娜·舒特勒 / 伊莎贝尔·奥特曼 / Jella Haase / Marietta Jemmi / Peter Jecklin','类型: 剧情 / 家庭','官方网站: www.heidi.studiocanal.de','制片国家/地区: 德国 / 瑞士','语言: 德语 / 瑞士德语','上映日期: 2015-12-10(德国) / 2016-02-10(法国)','片长: 111分钟','又名: 飘零燕(港) / 海蒂 / 阿尔卑斯山少女海蒂','IMDb链接: tt3700392','dirinfo')"
# cursor.execute(sql)

conn.close()