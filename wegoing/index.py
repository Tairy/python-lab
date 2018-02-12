#!usr/bin/env python
#coding=utf-8

import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('./jump/1050.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
width, height = gray.shape
gray = gray[640 : 1280, 0 : width]
thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]

# for w in range(width):
#   for h in range(height):
#     if(gray[w, h] >= 160 and gray[w, h] <= 200):
#       gray[w, h] = 0
#     else: 
#       gray[w, h] = 255

cv2.imwrite("result/3.jpeg", thresh)
    # print(gray[w, h])
# print(gray.shape)
# print(gray.shape())
# thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.imwrite("result/1.jpeg", gray)
# cv2.imwrite("result/2.jpeg", thresh)
# ret,th1 = cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)
# th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
# cv2.THRESH_BINARY,11,2) #换行符号 \
# th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
# cv2.THRESH_BINARY,11,2) #换行符号 \
# images = [img,th1,th2,th3]
# plt.figure()
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
# plt.show()
# cv2.imshow('image',thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#84aebe rgb(132,174,190)
#93ffb1 rgb(147,255,177)
#28ddd4 rgb(40,221,212)
#rgb(162,162,162) yuan
#454445 rgb(69,68,69)
#rgb(210,210,210)
#rgb(220,220,220)
#rgb(186,186,186)