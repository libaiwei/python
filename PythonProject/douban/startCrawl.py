# -*- coding:utf-8 -*-
__author__ = 'baiweili'
import crawl_douban_demo
import getMovieUrl
import Tkinter as tk
import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='lbw',
         host='127.0.0.1',
         database='douban')
cursor = conn.cursor()

def submit():
    try:
        start = int(num1.get())-1
        end = int(num2.get())
        num = end - start
        valueslist = []
        if num >= 0:
            print '电影排名从第' + str(start+1) + '名到第' + str(end) + '名'
            num = int(end)-int(start)
            spider = crawl_douban_demo.DouBan()
            urllist = getMovieUrl.getMovieURL(num,start)
            for url in urllist:
                values = spider.start(url)
                valueslist.append(values)
                print values
            # sql = ','.join(values)
        else:
            print '输入错误，前者小于后者！'
        for sql in valueslist:
            cursor.execute(sql)
        conn.close()
    except:
        print '输入错误，请重新输入整数！'

root = tk.Tk()

root.title("豆瓣电影信息抓取")
frame = tk.Frame(root)
frame.pack(padx=8, pady=8, ipadx=4)
lab1 = tk.Label(frame, text="排名:")
lab1.grid(row=0, column=0, padx=5, pady=5, sticky='W')
#绑定对象到Entry
num1 = tk.StringVar()
ent1 = tk.Entry(frame, textvariable=num1)
ent1.grid(row=0, column=1, sticky='ew', columnspan=1)
lab1_1 = tk.Label(frame, text="到")
lab1_1.grid(row=0, column=2, padx=5, pady=5, sticky='W')
num2 = tk.StringVar()
ent1_1 = tk.Entry(frame, textvariable=num2)
ent1_1.grid(row=0, column=3, sticky='ew', columnspan=3)
# lab2 = tk.Label(frame, text="显示:")
# lab2.grid(row=1, column=0, padx=5, pady=5, sticky='W')
p = tk.StringVar()
# ent2 = tk.Entry(frame, textvariable=p)
# ent2.grid(row=1, column=1, sticky='ew', columnspan=2)
button = tk.Button(frame, text="确定", command=submit, default='active')
button.grid(row=2, column=1)
lab3 = tk.Label(frame, text="")
lab3.grid(row=2, column=0, sticky='W')
button2 = tk.Button(frame, text="退出", command=quit)
button2.grid(row=2, column=3, padx=5, pady=5)
#以下代码居中显示窗口
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.mainloop()




# spider = crawl_douban_demo.DouBan()
# urllist = getMovieUrl.getMovieURL()
# for url in urllist:
#     values = spider.start(url)
#     print values
