#!usr/bin/env python
#coding=utf-8

import cv2
import numpy as np
import queue

camera = cv2.VideoCapture(0)
width = int(camera.get(3))
height = int(camera.get(4))

# firstGrabbed, firstFrame = camera.read()
# firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
# p0 = cv2.goodFeaturesToTrack(firstFrame, mask = None, **feature_params)
firstFrame = None
lastDec = None
firstThresh = None

feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0,255,(100,3))
num = 0

# cursor_x = []
# cursor_y = []

q_x = queue.Queue(maxsize = 10)
q_y = queue.Queue(maxsize = 10)

while True:
  (grabbed, frame) = camera.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  if firstFrame is None:
    firstFrame = gray
    continue

  frameDelta = cv2.absdiff(firstFrame, gray)
  thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
  # thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            # cv2.THRESH_BINARY,11,2)
  # thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
  #           cv2.THRESH_BINARY,11,2)
  thresh = cv2.dilate(thresh, None, iterations=2)
  p0 = cv2.goodFeaturesToTrack(thresh, mask = None, **feature_params)
  if p0 is not None:
    x_sum = 0
    y_sum = 0
    for i, old in enumerate(p0):
      x, y = old.ravel()
      x_sum += x
      y_sum += y
    x_avg = x_sum / len(p0)
    y_avg = y_sum / len(p0)
    
    if q_x.full():
      # print list(q_x.queue)
      qx_list = list(q_x.queue)
      key = 0
      diffx_sum = 0
      for item_x in qx_list:
        key +=1
        if key < 10:
          diff_x = item_x - qx_list[key]
          diffx_sum += diff_x
          # print diff_x
      # if diffx_sum < 0 and x_avg < 500:
      if diffx_sum < 0:
        # print "some coming form left"
        print("left")
        # cv2.putText(frame, "left", (100,100), 0, 0.5, (0,0,255),2)
      else:
        # cv2.putText(frame, "right", (100,100), 0, 0.5, (0,0,255),2)
        print("right")

      # print x_avg
      #   print key
      q_x.get()
    q_x.put(x_avg)
    cv2.putText(frame, str(x_avg), (300,100), 0, 0.5, (0,0,255),2)
    frame = cv2.circle(frame,(int(x_avg),int(y_avg)),5,color[i].tolist(),-1)
    # print x_avg
    # print y_avg
      # frame = cv2.circle(frame,(c,d),5,color[i].tolist(),-1)
  # print num
  # print p0
  # for i,(new,old) in enumerate(zip(good_new,good_old)):

  # frame = cv2.circle(frame,(p0[0],p0[1]),5,color[1].tolist(),-1)

  # print p0

  # if firstThresh is None:
  #   firstThresh = thresh
  #   p0 = cv2.goodFeaturesToTrack(firstThresh, mask = None, **feature_params)
  #   mask = np.zeros_like(firstThresh)
  #   continue


  # p1, st, err = cv2.calcOpticalFlowPyrLK(firstThresh, thresh, p0, None, **lk_params)
  
  # print p1
  # if p1 is not None:
  #   for i,(old) in enumerate(p1):
  #     c,d = old.ravel()
  #     frame = cv2.circle(frame,(c,d),5,color[i].tolist(),-1)
  # if p1 is not None:
  #   good_new = p1[st==1]
  #   good_old = p0[st==1]

  #   print good_old
  #   print good_new

  # #   # draw the tracks
  #   for i,(new,old) in enumerate(zip(good_new,good_old)):
  #     a,b = new.ravel()
  #     c,d = old.ravel()
  #     frame = cv2.line(frame, (a,b),(c,d), color[i].tolist(), 2)
  #     frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)

  # img = cv2.add(frame,mask)

  
  # print p0
  # (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
  # cnt_num = 0
  # x_sum = 0
  # y_sum = 0

  # for c in cnts:
  #   if cv2.contourArea(c) < 10000:
  #     continue

  #   # print cv2.contourArea(c)
  #   (x, y, w, h) = cv2.boundingRect(c)
  #   cnt_num += 1
  #   x_sum += x
  #   y_sum += y

  #   cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

  cv2.imshow("Security Feed", frame)
  # print q_x.qsize()
  # print q_y.qsize()
  firstFrame = gray.copy()
  # firstThresh = thresh.copy()
  # num += 1
  # p0 = good_new.reshape(-1,1,2)

camera.release()
cv2.destroyAllWindows()