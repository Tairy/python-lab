# encoding:utf-8
import os

files = []
for item in os.walk('./valid_set/'):
  files = item[2]
  i = 0
  for file in files:
    if(i % 2 == 0):
      os.renames('./splits/' + file, './train_set/' + file)
    i += 1
  break