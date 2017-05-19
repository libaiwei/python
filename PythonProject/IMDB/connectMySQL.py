# -*- coding:utf-8 -*-
import mysql.connector
def connect():
    conn = mysql.connector.connect(
        user='root',
        password='lbw',
        host='localhost',
        database='douban')
    cursor = conn.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS IMDB")

    sql = """CREATE TABLE IMDB (
        RANK  INT(10) NOT NULL,
        MOVIE  CHAR(40) NOT NULL,
        YEAR CHAR(20),
        DIRECTOR  CHAR(40),
        WRITER CHAR(100),
        STARS CHAR(100),
        BIRTHDAY CHAR(40),
        PALACE CHAR(100))"""
    cursor.execute(sql)
    conn.close()
if __name__ == '__main__':
    connect()