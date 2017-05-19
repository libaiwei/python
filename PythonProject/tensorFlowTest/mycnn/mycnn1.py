#coding:utf8
import xlrd
import tensorflow as tf
import cv2
from matplotlib import pyplot as plt
import random
import numpy as np
import scipy.io as sio

def getdata(file):
    #get image and label
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    nrows = table.nrows
    images = []
    labels = []
    path = '/Users/lbw/Desktop/Agg_AMT_Candidates/'
    for i in xrange(0,nrows,5):
        image = str(table.row_values(i)[0]).split('/')[-1]
        label = 0.0
        for j in xrange(5):
            label += float(table.row_values(i+j)[1])
        if label > 3.0:
            label = [1,0]
        else:
            label = [0,1]
        labels.append(label)
        img = path+image
        image0 = cv2.imread(img)
        # plt.imshow(image0, cmap='gray', interpolation='bicubic')
        # plt.xticks([]), plt.yticks([])
        # plt.show()
        dim =(256,256)           #指定尺寸w*h
        resized =cv2.resize(image0,dim,interpolation = cv2.INTER_AREA)
        images.append(resized)

        # 展示裁剪效果
        # imageorigin = cv2.imread(img)
        # showimages = [imageorigin, image0, resized]
        # titles = ['a', 'b', 'c']
        # for i in xrange(3):
        #     plt.subplot(1, 3, i + 1), plt.imshow(showimages[i], 'gray')
        #     plt.title(titles[i])
        #     plt.xticks([]), plt.yticks([])
        # plt.show()
    return images,labels



batch_size = 50
def getbatch(images, labels, batch_size):
    length = len(images)
    index = random.sample(range(length), batch_size)
    img_srt = []
    lab_srt = []
    for i in index:
        a = images[i]
        img_srt.append(a)
        lab_srt.append(labels[i])
    img_srt = np.array(img_srt)
    lab_srt = np.array(lab_srt)
    return (img_srt, lab_srt)
train, train_labels = getdata('/Users/lbw/Desktop/img2.xlsx')
test, test_labels = getdata('/Users/lbw/Desktop/img1.xlsx')
sio.savemat('data.mat', {'train': train,'train_labels': train_labels,'test': test,'test_labels': test_labels})
# batch = getbatch(images, labels, 50)
# print batch[0]