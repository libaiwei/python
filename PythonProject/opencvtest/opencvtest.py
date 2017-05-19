import cv2
import numpy as np
from matplotlib import pyplot as plt

#coding:utf8
#open image
# img = cv2.imread('/Users/lbw/Desktop/user.png')
# # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
# # cv2.imshow('Image',img)
# # k = cv2.waitKey(0)
# # if k == 27:
# #     cv2.destroyAllWindows()
#
# plt.imshow(img, cmap='gray', interpolation='bicubic')
# plt.xticks([]), plt.yticks([])
# plt.show()

#open video

# #open a camera
# cap = cv2.VideoCapture(0)
# while(True):
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     cv2.imshow('frame', gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

#save video
cap = cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1280,720))
while(cap.isOpened()):
    ret, frame = cap.read()
    # print type(frame),frame.shape
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if ret == True:
        frame = cv2.flip(frame, 0)
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()