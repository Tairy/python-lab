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

cap = cv2.VideoCapture('./jbc.avi')
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# y = np.random.randint(1,100,40)
# y = y.reshape((5,8))
# print(y)
# df = pd.DataFrame(y,columns=[x for x in 'abcdefgh'])
# sns.heatmap(df,annot=True)
# plt.show()

# exit(0)
width = 30
height = 30
# width = 332
# height = 424
arr = np.zeros((height, width))
# print(arr)
# exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
      break
      # cap = cv2.VideoCapture('./jbc.avi')
      # continue
    # origin_center = frame[120:150, 200:230]
    # origin_center = cv2.cvtColor(origin_center, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    center = gray[120:150, 200:230]

    p0 = cv2.goodFeaturesToTrack(center, mask = None, **feature_params)
    if p0 is not None:
      x_sum = 0
      y_sum = 0
      for i, old in enumerate(p0):
        x, y = old.ravel()
        x_sum += x
        y_sum += y
      x_avg = int(x_sum / len(p0))
      y_avg = int(y_sum / len(p0))
      # print(x_avg, y_avg)
      # center = cv2.cvtColor(center, cv2.COLOR_GRAY2RGB)
      # cv2.circle(frame,(x_avg + 200,y_avg + 120),4,(0,0,255),5)
      # arr[y_avg + 120, x_avg + 200] += 1
      arr[y_avg, x_avg] += 1
      # print(y_avg + 120, x_avg + 200)
    # print(len(p0))
    # cnts = cv2.findContours(center, cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)[-2]

    # for c in cnts:
    #   # approximate the contour
    #   # peri = cv2.arcLength(c, True)
    #   # approx = cv2.approxPolyDP(c, 0.02 * peri, True)
     
    #   # # if our approximated contour has four points, then
    #   # # we can assume that we have found our screen
    #   # if len(approx) == 4:
    #   #   screenCnt = approx
    #   #   break
    #   cv2.drawContours(center, c, -1, (255, 0, 0), 3)

    # print(cnts)
    # cv2.rectangle(gray, (180,85), (260,170), (0,0,255), 1)
    # time.sleep(2)
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
cap.release()
plt.matshow(arr, cmap='hot')
plt.colorbar()
plt.show()
# print(arr)
# df = pd.DataFrame(arr, columns=[x for x in range(width)])
# sns.heatmap(df, annot=True)
# plt.show()
# cv2.destroyAllWindows()
