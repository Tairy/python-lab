# encoding:utf-8
import os
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('./p0-45mW-new1.wmv')

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

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

  center = gray[600:630, 795:825]
  origin_center = frame[600:630, 795:825]

  im2, contours, hierarchy = cv2.findContours(center, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) >= 2:
    # cnt = max(contours, key = cv2.contourArea)
    cnt = contours[1]
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(origin_center,(cx,cy), 1, (0,255,0), -1)
    # print(cx, cy)
    arr[cx, cy] += 1
    # x,y,w,h = cv2.boundingRect(cnt)
    # # cv2.rectangle(frame,(795 + x, 600 + y),(795 + x + w, 600 + y + h),(0,255,0),1)
    # cv2.rectangle(origin_center, (x, y), (x + w, y + h), (0,255,0), 1)
    # _center = (x + w) / 2, (y + h) / 2
    # a_x = int(((x + w) / 2))
    # a_y = int(((y + h) / 2))
    # arr[a_x, a_y] += 1
    # print(a_x, a_y)
    # print(_center)
    # cv2.drawContours(origin_center, contours, 1, (0, 0, 255), 1)
    # for cnt in contours:
    #   x,y,w,h = cv2.boundingRect(cnt)
    #   cv2.rectangle(origin_center,(x,y),(x+w,y+h),(0,255,0),1)
    # (x,y),radius = cv2.minEnclosingCircle(cnt)
    # _center = (int(x),int(y))

    # print(_center)
    # radius = int(radius)
    # print(radius)
    # cv2.circle(origin_center,_center,radius,(0,255,0),1)

  cv2.imshow("capture", origin_center)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()
# cap.release()
# plt.matshow(arr, cmap='hot')
# plt.colorbar()
# plt.show()