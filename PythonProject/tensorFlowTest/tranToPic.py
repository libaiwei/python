# coding=utf8
from PIL import Image as img
import numpy as np

def extractfile(f):
    #读取数据
    LABEL_SIZE = 1
    IMAGE_SIZE = 32
    NUM_CHANNELS = 3
    PIXEL_DEPTH = 255

    TRAIN_NUM = 10000
    bytestream=open(f,'rb')
    #读取数据，首先将数据集中的数据读取进来作为buf
    buf = bytestream.read(TRAIN_NUM * (IMAGE_SIZE * IMAGE_SIZE * NUM_CHANNELS+LABEL_SIZE))
    #把数据流转化为np的数组,为什么要转化为np数组呢，因为array数组只支持一维操作，为了满足我们的操作需求，我们利用np.frombuffer()将buf转化为numpy数组现在data的shape为（30730000，），3073是3*1024+1得到的，3个channel（r，g，b），每个channel有1024=32*32个信息，再加上 1 个label

    data = np.frombuffer(buf, dtype=np.uint8)

    #改变数据格式,将shape从原来的（30730000，）——>为（10000，3073）
    data = data.reshape(TRAIN_NUM,LABEL_SIZE+IMAGE_SIZE* IMAGE_SIZE* NUM_CHANNELS)

    #分割数组,分割数组，np.hsplit是在水平方向上，将数组分解为label_size的一部分和剩余部分两个数组，在这里label_size=1，也就是把标签label给作为一个数组单独切分出来如果你对np.split还不太了解，可以自行查阅一下，此时label_images的shape应该是这样的[array([.......]) , array([.......................])]
    labels_images = np.hsplit(data, [LABEL_SIZE])

    label = labels_images[0].reshape(TRAIN_NUM)#此时labels_images[0]就是我们上面切分数组得到的第一个数组，在这里就是label数组，这时的shape为array([[3] , [6] , [4] , ....... ,[7]])，我们把它reshape（）一下变为了array([3 , 6 , ........ ,7])

    image = labels_images[1].reshape(TRAIN_NUM,IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS)#此时labels_image[1]就是我们上面切分数组的剩余部分，也就是图片部分我们把它reshape（）为（10000，32，32，3）

    #合并数组，不能用加法
    # labels = np.concatenate((labels,label))
    # images = np.concatenate((images,image))
    labels = label
    images = image

    # images = (images - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH

    return labels,images

labels,images = extractfile('/tmp/cifar10_data/cifar-10-batches-bin/data_batch_1.bin')
pic_1 = images[0,0:32,0:32,0:3]
# a=np.reshape(pic_1,[32*32,3])
# contract = np.ones([32*32,1],dtype=np.int)*255
# c = np.hstack((a,contract))
# pic_1 = np.reshape(c,[32,32,4])
# print pic_1

# def MatrixToImage(data):
#     new_im = img.fromarray(data.astype(np.uint8))
#     return new_im
# new_im = MatrixToImage(pic_1)
# print pic_1.shape
# new_im.save('/Users/baiweili/Desktop/2.jpg')


arrayGray2Image = img.fromarray(pic_1)
arrayGray2Image.save('aa.jpg')