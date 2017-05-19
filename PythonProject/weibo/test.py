#coding:utf8
def fun(num):
 for i in range(num):
  if i < num / 2:
   print('' * i)
  else:
   print('' * (num-i))

fun(90)
