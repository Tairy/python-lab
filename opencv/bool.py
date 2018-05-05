# encoding:utf-8
import os
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

'''
识别视频中运动的点
'''

cap = cv2.VideoCapture('./42.8mW-P0-single particle_0.avi')

width = 50
height = 50
arr = np.zeros((height, width))
index = 0
times = 0
while True:
  ret, frame = cap.read()
  if ret == False:
    break
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  center = gray[70:120, 85:145]
  origin_center = frame[70:120, 85:135]
  index += 1
  if index >= 1300:
    continue
  im2, contours, hierarchy = cv2.findContours(center, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) != 0:
    #find the biggest area
    cnt = max(contours, key = cv2.contourArea)
    cv2.drawContours(im,contours,-1,(0,255,0),3)
    # cv2.drw
    # M = cv2.moments(cnt)
    # if M['m00'] > 0:
    #   cx = int(M['m10']/M['m00'])
    #   cy = int(M['m01']/M['m00'])
    #   #print(cx, cy)
    #   cv2.circle(origin_center,(cx,cy), 1, (0,0,255), 1)
    # # print(cx, cy)
    #   arr[cx, cy] += 1
  # # movie
  cv2.imshow("capture", center)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()

#--- draw hot image
# cv2.destroyAllWindows()
# cap.release()
# plt.matshow(arr, cmap='hot')
# plt.colorbar()
# plt.show() 