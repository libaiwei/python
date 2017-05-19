#coding:utf8
import numpy as np
from PIL import Image as img

def countnum(data):#返回高维数组的元素的个数
    dshape = data.shape
    num=1
    for i in range(len(dshape)):
        num *= dshape[i]
    return num
#获取图像的RGB数据，保存为数组
rgb = np.array(img.open('/Users/baiweili/Desktop/1.png'))
#获取图像的灰度数据，保存为数组
gray = np.array(img.open('/Users/baiweili/Desktop/1.png').convert('L'))
#数据的维度，前者是三维的，后者是二维的
print "由图像得到的数组:",rgb.shape,gray.shape
#RGB数据元素个数
numrgb = countnum(rgb)
#灰度数据元素个数
numgray = countnum(gray)
#将图像数据保存成一维数据
rgb1 = rgb.reshape(numrgb,1)
gray1 = gray.reshape(numgray,1)
print "由图像得到的数组转换成一维后:",rgb1.shape,gray1.shape
#获取RGB图像的维度信息
d1,d2,d3 = rgb.shape
#根据维度信息和一维数组恢复RGB的三维数组
rgb = rgb1.reshape(d1,d2,d3)
#获取灰度图像的维度信息
d1,d2 = gray.shape
#根据维度信息和一维数组恢复灰度的二维数组
gray = gray1.reshape(d1,d2)
print "从一维恢复到原来的维度:",rgb.shape,gray.shape
#将灰度的二维数组保存成图像
arrayGray2Image = img.fromarray(gray)
arrayGray2Image.save('aa.jpg')
#将RGB的三维数组保存成图像
arrayRGB2Image = img.fromarray(rgb)
arrayRGB2Image.save('bb.jpg')
#读取保存的图像数据信息，查看是否有损失，答案是没有
rgb = np.array(img.open('aa.jpg'))
gray = np.array(img.open('bb.jpg').convert('L'))
print "由数组重新生成的图像得到的数组:",rgb.shape,gray.shape


