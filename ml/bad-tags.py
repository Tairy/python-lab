#!/usr/bin/python
# -*- coding: UTF-8 -*-

file = open("../data/tag_sort_by_rank.txt")
target_file = open("../data/target_file_1.txt", "w+")
tags = file.readlines()
for tag in tags:
  splitTag = tag.split()
  print splitTag[1]
  # if(len(splitTag) >= 3 and int(splitTag[2]) >= 1):
  #   target_file.write(tag)

file.close()
target_file.close()


