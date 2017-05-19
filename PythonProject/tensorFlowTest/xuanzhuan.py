#coding:utf-8
import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread("/Users/lbw/Desktop/3.jpeg")
dim =(500,500)           #指定尺寸w*h
image =cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
rows,cols,channel = image.shape

M = cv2.getRotationMatrix2D((cols/2,rows/3),90,1)
dst = cv2.warpAffine(image,M,(cols,rows))
# cv2.imshow("Original",image)
# cv2.waitKey(0)
(h,w) = image.shape[:2]
center = (w / 2,h / 2)

M = cv2.getRotationMatrix2D(center,315,1)#旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
rotated_4 = cv2.warpAffine(image,M,(w,h))
#旋转45度，缩放0.75
M = cv2.getRotationMatrix2D(center,45,1)#旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
rotated_1 = cv2.warpAffine(image,M,(w,h))
# cv2.imshow("Rotated by 45 Degrees",rotated)
# cv2.waitKey(0)
#旋转-45度，缩放1.25
M = cv2.getRotationMatrix2D(center,135,1)#旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
rotated_2 = cv2.warpAffine(image,M,(w,h))
#旋转-45度，缩放1.25
M = cv2.getRotationMatrix2D(center,225,1)#旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
rotated_3 = cv2.warpAffine(image,M,(w,h))
# cv2.imshow("Rotated by -90 Degrees",rotated)
# cv2.waitKey(0)
flipped = cv2.flip(image,1)
flipped_1 = cv2.flip(image,0)
flipped_2 = cv2.flip(image,-1)
result = []
r = np.hstack((rotated_3,rotated_2))
r1 = np.hstack((rotated_4,rotated_1))
r2 = np.row_stack([r,r1])
for i in range(1):
    r = np.hstack((r2,r2))
    r2 = np.row_stack((r,r))
dim =(500,500)           #指定尺寸w*h
r2 =cv2.resize(r2,dim,interpolation = cv2.INTER_AREA)
result = (np.array(result)).T
cv2.imshow("Original",r2)
cv2.waitKey(0)
# # result_1 = result.reshape(579,1110,3)
# print result.shape
# showimages = [r2]
# # titles = ['a', 'b', 'c']
# for i in xrange(1):
#     # fig = plt.figure(figsize=(1, 3))
#     plt.subplots_adjust(left=0., bottom=0., right=0.8, top=0.8, hspace = 0., wspace = 0.)
#     plt.subplot(1, 1, i + 1), plt.imshow(showimages[i])
#
#     # plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()