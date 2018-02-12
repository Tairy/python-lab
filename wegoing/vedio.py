#!usr/bin/env python
#coding=utf-8

import numpy as np
import cv2

cap = cv2.VideoCapture('model1.mp4')

i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    # img_name = "1-" + str(i) + ".jpeg"
    # cv2.imwrite("images/"+img_name, frame)
    # print(img_name)
    # i += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    width, height = gray.shape
    gray = gray[500 : 1280, 0 : width]
    thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('frame',thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()