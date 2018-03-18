# encoding:utf-8
import os
import cv2
import numpy as np

cap = cv2.VideoCapture('./game.mp4')

index = 0
firstFrame = None

while True:
  ret, frame = cap.read()
  if ret == False:
    break

  index += 1

  if index < 350:
    continue

  origin_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  width, height = origin_gray.shape
  gray = origin_gray[400 : 1280, 0 : width]
  origin_frame = frame[400 : 1280, 0 : width]
  
  thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

  im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contours:
    c_len = len(c)
    c_area = cv2.contourArea(c)

    if c_len in range(80, 100) and c_area in range(1100, 1200):
      (x, y), radius = cv2.minEnclosingCircle(c)
      center = (int(x), 400 + int(y))
      radius = int(radius)
      if radius in [27, 28]:
        cv2.circle(frame, center, radius, (0, 255, 0), 100)

  img = cv2.resize(frame, (int(height / 3), int(width / 3)), interpolation=cv2.INTER_CUBIC)

  cv2.imshow("capture", img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()