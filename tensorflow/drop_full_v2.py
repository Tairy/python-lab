# encoding:utf-8
import os
import cv2
import numpy as np
import argparse
from itertools import groupby
from os.path import basename

"""
大水滴惯性分割算法
1. 找到 start_point
"""

def drop_fall(image):
  
