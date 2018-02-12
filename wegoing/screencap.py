#!usr/bin/env python
#coding=utf-8

import os
import cv2

while True:
  os.system('adb shell screencap -p /sdcard/autojump.png')
  os.system('adb pull /sdcard/autojump.png ./screencap/screencap.png')
  img = cv2.imread('./screencap/screencap.png')
  small = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
  cv2.imshow('frame', small)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break