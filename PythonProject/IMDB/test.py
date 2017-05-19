# -*- coding:utf-8 -*-
import mysql.connector
def connect(sql):
    conn = mysql.connector.connect(
        user='root',
        password='123',
        host='10.110.150.231',
        database='libaiwei')
    cursor = conn.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    # cursor.execute("DROP TABLE IF EXISTS IMDB")
    #
    # sql = """CREATE TABLE IMDB (
    #     RANK  INT(10) NOT NULL,
    #     MOVIE  CHAR(40) NOT NULL,
    #     YEAR CHAR(20),
    #     DIRECTOR  CHAR(40),
    #     WRITER CHAR(100),
    #     STARS CHAR(100),
    #     BIRTHDAY CHAR(40),
    #     PALACE CHAR(100))"""
    sql = 'insert into IMDB values'+'(1,"The Shawshank Redemption","1994","Frank Darabont","Stephen King,Frank Darabont","Tim Robbins,Morgan Freeman,Bob Gunton","1959-1-28","Montbéliard, Doubs, France")'
    cursor.execute(sql)
    conn.close()
if __name__ == '__main__':
    connect('')