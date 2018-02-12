#!usr/bin/env python
#coding=utf-8
import os
import cv2

files = []
for item in os.walk('./images/'):
  files = item[2]
  i = 0
  for file in files:
    if cv2.waitKey(0) & 0xFF == ord('q'):
      break
    img = cv2.imread('./images/' + file)
    small = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    cv2.imshow('frame', small)
    if cv2.waitKey(0) & 0xFF == ord('y'):
      os.renames('./images/' + file, './jump/2-' + file)
    else:
      continue
  break