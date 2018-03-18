# encoding:utf-8
import os
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

'''
识别视频中运动的点
'''

cap = cv2.VideoCapture('./3.avi')
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7)

width = 30
height = 30
arr = np.zeros((height, width))
index = 0
times = 0
while True:
  ret, frame = cap.read()
  if ret == False:
    break
    # index = 0
    # times += 1
    # if times >= 10:
      # break
    # cap = cv2.VideoCapture('./3.avi')
    # continue
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

  # 2.avi
  # center = gray[90:120, 100:130]
  # origin_center = frame[90:120, 100:130]
  
  # 3.avi
  center = gray[70:130, 80:140]
  origin_center = frame[70:130, 80:140]


  index += 1
  # if index > 1200:
    # continue
#   print(index)
  if index > 1080 or index < 530:
    continue
#   cv2.imshow("capture", center)
#   if cv2.waitKey(1) & 0xFF == ord('q'):
#     break
# cap.release()
# cv2.destroyAllWindows()

  im2, contours, hierarchy = cv2.findContours(center, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) != 0:
    # draw in blue the contours that were founded

    #find the biggest area
    cnt = max(contours, key = cv2.contourArea)

    # cv2.drawContours(origin_center, [c], -1, (0, 0, 255), 2)
    # cv2.drawContours(origin_center, contours, -1, (0, 0, 255), 2)
    # ellipse = cv2.fitEllipse(cnt)
    # cv2.ellipse(origin_center,ellipse,(0,255,0))
    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(origin_center,[box],0,(0, 0, 255), 2)
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    _center = (int(x),int(y))
    print(_center)
    # for _x in range(-1, 1):
    #   for _y in range(-1, 1):
    #     arr[int(y) + _y, int(x) + _x] += 1
    # if int(y) in range(5, 20) or int(x) in range(5, 25):
      # arr[int(y), int(x)] += 1

    # print(center)
    radius = int(radius)
    cv2.circle(origin_center,_center,radius,(0,255,0),1)


#     # x,y,w,h = cv2.boundingRect(c)
#     # draw the book contour (in green)
#     # cv2.rectangle(origin_center,(x,y),(x+w,y+h),(0,255,0),2)
#   # print(contours)
#   # print(len(contours))
#   # cv2.drawContours(origin_center, contours, -1, (0, 0, 255), 2)

#   # p0 = cv2.goodFeaturesToTrack(center, mask = None, **feature_params)
#   # if p0 is not None:
#   #   x_sum = 0
#   #   y_sum = 0
#   #   for i, old in enumerate(p0):
#   #     x, y = old.ravel()
#   #     x_sum += x
#   #     y_sum += y
#   #   x_avg = int(x_sum / len(p0))
#   #   y_avg = int(y_sum / len(p0))
#   #   for x in range(-2, 2):
#   #     for y in range(-2, 2):
#   #       arr[y_avg + y, x_avg + x] += 1
#     # arr[y_avg, x_avg] += 1
#     # cv2.circle(origin_center,(x_avg,y_avg),2,(0,255,0),2)
  cv2.imshow("capture", origin_center)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()

# arr = arr[20:50, 15:45]
# cap.release()
# plt.matshow(arr, cmap='hot')
# plt.colorbar()
# plt.show()