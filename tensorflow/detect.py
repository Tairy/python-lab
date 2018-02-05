# encoding:utf-8
import os
import cv2
import numpy as np
import argparse
from itertools import groupby
from os.path import basename
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import batch_normalization
from tflearn.layers.estimator import regression

IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20
CODE_LEN = 1
MAX_CHAR = 10
LOG_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/tflog/"
CHECK_POINT = "/Users/tairy/Documents/Working/python-lab/tensorflow/check_point/"

def get_projection_x(image):
    height, width = image.shape[:2]
    p_x = [0 for _ in range(width)]

    for x in range(width):
        for y in range(height):
            if image[y, x] == 0:
                p_x[x] += 1
    return p_x


def get_start_x(hist_width, divide):
    """
    根据待切割的图片的竖直投影统计hist_width，找到合适的滴水起始点
    hist_width的中间值，前后再取4个值，在这个范围内找最小值
    """
    mid = int(len(hist_width) / divide)
    # 共9个值
    return mid - 4 + np.argmin(hist_width[mid - 4:mid + 5])


def get_end_route(image, start_x, height):
    """
    获得滴水的路径
    : param start_x: 滴水的起始x位置
    """
    left_limit = 0
    right_limit = image.shape[1] - 1

    end_route = []
    cur_p = (start_x, 0)
    last_p = cur_p
    end_route.append(cur_p)

    while cur_p[1] < (height - 1):
        sum_n = 0
        maxW = 0  # max Z_j*W_j
        nextX = cur_p[0]
        nextY = cur_p[1]
        for i in range(1, 6):
            curW = get_nearby_pixel_val(image, cur_p[0], cur_p[1], i) * (6 - i)
            sum_n += curW
            if maxW < curW:
                maxW = curW

        # 如果全黑，需要看惯性
        if sum_n == 0:
            maxW = 4

        # 如果全白，则默认垂直下落
        if sum_n == 15:
            maxW = 6

        if maxW == 1:
            nextX = cur_p[0] - 1
            nextY = cur_p[1]
        elif maxW == 2:
            nextX = cur_p[0] + 1
            nextY = cur_p[1]
        elif maxW == 3:
            nextX = cur_p[0] + 1
            nextY = cur_p[1] + 1
        elif maxW == 5:
            nextX = cur_p[0] - 1
            nextY = cur_p[1] + 1
        elif maxW == 6:
            nextX = cur_p[0]
            nextY = cur_p[1] + 1
        elif maxW == 4:
            if nextX > cur_p[0]:  # 具有向右的惯性
                nextX = cur_p[0] + 1
                nextY = cur_p[1] + 1

            if nextX < cur_p[0]:
                nextX = cur_p[0]
                nextY = cur_p[1] + 1

            if sum_n == 0:
                nextX = cur_p[0]
                nextY = cur_p[1] + 1
        else:
            raise Exception("get a wrong maxW, pls check")

        # 如果出现重复运动
        if last_p[0] == nextX and last_p[1] == nextY:
            if nextX < cur_p[0]:
                maxW = 5
                nextX = cur_p[0] + 1
                nextY = cur_p[1] + 1
            else:
                maxW = 3
                nextX = cur_p[0] - 1
                nextY = cur_p[1] + 1

        last_p = cur_p

        if nextX > right_limit:
            nextX = right_limit
            nextY = cur_p[1] + 1

        if nextX < left_limit:
            nextX = left_limit
            nextY = cur_p[1] + 1

        cur_p = (nextX, nextY)
        end_route.append(cur_p)

    # 返回分割路径
    return end_route


def get_nearby_pixel_val(image, cx, cy, j):
    size = image.shape[:2]
    if cx + 1 >= size[1] or cy + 1 >= size[0]:
        return 1
    if j == 1:
        return 0 if sum(image[cy + 1, cx - 1]) == 0 else 1
    elif j == 2:
        return 0 if sum(image[cy + 1, cx]) == 0 else 1
    elif j == 3:
        return 0 if sum(image[cy + 1, cx + 1]) == 0 else 1
    elif j == 4:
        return 0 if sum(image[cy, cx + 1]) == 0 else 1
    elif j == 5:
        return 0 if sum(image[cy, cx - 1]) == 0 else 1
    else:
        raise Exception("what you request is out of nearby range")


def do_split(source_image, starts, filter_ends):
    """
    具体实行切割
    : param starts: 每一行的起始点 tuple of list
    : param ends: 每一行的终止点
    """
    left = starts[0][0]
    top = starts[0][1]
    right = filter_ends[0][0]
    bottom = filter_ends[0][1]

    for i in range(len(starts)):
        left = min(starts[i][0], left)
        top = min(starts[i][1], top)
        right = max(filter_ends[i][0], right)
        bottom = max(filter_ends[i][1], bottom)

    width = right - left + 1
    height = bottom - top + 1

    image = np.zeros((height, width, 3), np.uint8)

    for i in range(height):
        start = starts[i]
        end = filter_ends[i]
        for x in range(start[0], end[0] + 1):
            if sum(source_image[start[1], x]) == 0:
                image[start[1] - top, x - left] = [0, 0, 0]
            else:
                image[start[1] - top, x - left] = [255, 255, 255]

    return image


def get_black_border(image):
    """
    获取指定图像的内容边界坐标
    :param image: 图像 Image Object
    :return: 图像内容边界坐标tuple (left, top, right, bottom)
    """
    height, width = image.shape[:2]
    max_x = max_y = 0
    min_x = width - 1
    min_y = height - 1
    for y in range(height):
        for x in range(width):
            if sum(image[y, x]) == 0:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    return [min_x, min_y, max_x + 1, max_y + 1]


def drop_fall(image, divide):
    """
    对粘连两个字符的图片进行drop fall算法分割
    """
    # 1. 竖直投影统计
    height, width = image.shape[:2]
    # print("当前待切割图片的 width: %d, height: %d" % (width, height))
    hist_width = [0] * width
    for x in range(width):
        for y in range(height):
            if sum(image[y, x]) == 0:
                hist_width[x] += 1
    # 2. 找到极小值点
    start_x = get_start_x(hist_width, divide)
    # 3. 以这个极小值点作为起始滴落点,实施滴水算法
    start_route = []
    for y in range(height):
        start_route.append((0, y))

    end_route = get_end_route(image, start_x, height)
    filter_end_route = [max(list(k)) for _, k in groupby(end_route, lambda x: x[1])]
    img1 = do_split(image, start_route, filter_end_route)
    border1 = get_black_border(img1)
    start_route = list(map(lambda x: (x[0] + 1, x[1]), filter_end_route))
    end_route = []
    for y in range(height):
        end_route.append((width - 1, y))

    img2 = do_split(image, start_route, end_route)
    border2 = get_black_border(img2)
    border2[0] += start_x
    border2[2] += start_x
    return [border1, border2]


def adaptive_threshold(image):
    image = cv2.adaptiveThreshold(image, 100, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
    return image


def cnn():
    network = input_data(shape=[None, IMAGE_HEIGHT, IMAGE_WIDTH, 1], name='input')
    network = conv_2d(network, 8, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, CODE_LEN * MAX_CHAR, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='target')
    return network


def vec2text(vec):
    text = ''
    max_value = []
    for pos in range(CODE_LEN):
        max_value.append(np.max(vec[pos * MAX_CHAR:(pos + 1) * MAX_CHAR]))

    for i, v in enumerate(vec):
        if v == max_value[int(i / MAX_CHAR)]:
            text += chr(i % MAX_CHAR + ord('0'))
    return text


def split_image(image_name):
    base_path = './test_set/'
    # print("当前待切割图片:%s" % (image_name))
    img = cv2.imread(base_path + image_name)
    file_name = image_name.split('.')[0]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # loop over the contours
    max_x = 0
    max_y = 0
    min_x = 500
    min_y = 100

    for (i, c) in enumerate(cnts):
        for i_c in c:
            if max_x < i_c[0][0]:
                max_x = i_c[0][0]
            if max_y < i_c[0][1]:
                max_y = i_c[0][1]
            if min_x > i_c[0][0]:
                min_x = i_c[0][0]
            if min_y > i_c[0][1]:
                min_y = i_c[0][1]

    origin_split_image = img[min_y:max_y, min_x:max_x]
    split_image = thresh[min_y:max_y, min_x:max_x]
    split_image = cv2.cvtColor(split_image, cv2.COLOR_GRAY2RGB)


    x_batch = np.zeros([6, IMAGE_HEIGHT, IMAGE_WIDTH])

    for i in reversed(range(2, 7)):
        r_i = 6 - i
        borders = drop_fall(split_image, i)
        # child_img = origin_split_image[borders[0][1]:borders[0][3], borders[0][0]:borders[0][2]]
        child_img = split_image[borders[0][1]:borders[0][3], borders[0][0]:borders[0][2]]
        child_img = cv2.resize(child_img, (20, 20), interpolation=cv2.INTER_CUBIC)
        child_img = cv2.cvtColor(child_img, cv2.COLOR_RGB2GRAY)
        # child_img = cv2.cvtColor(child_img, cv2.COLOR_BGR2RGB)
        child_img = adaptive_threshold(child_img)
        x_batch[r_i, :] = child_img

        split_image = split_image[borders[1][1]:borders[1][3], borders[1][0]:borders[1][2]]
        # origin_split_image = origin_split_image[borders[1][1]:borders[1][3], borders[1][0]:borders[1][2]]
        if 2 == i:
            if len(split_image) > 0:
                # origin_split_image = cv2.resize(origin_split_image, (20, 20), interpolation=cv2.INTER_CUBIC)
                split_image = cv2.resize(split_image, (20, 20), interpolation=cv2.INTER_CUBIC)
                split_image = cv2.cvtColor(split_image, cv2.COLOR_RGB2GRAY)
                split_image = adaptive_threshold(split_image)
                # split_image = cv2.cvtColor(split_image, cv2.COLOR_GRAY2BGR)
                x_batch[5, :] = split_image
                # cv2.imwrite("predict_splits/" + file_name + "-5-5.jpeg", split_image)

    x_batch = x_batch.reshape([-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    return x_batch

def predict():
    files = []
    for item in os.walk('./test_set/'):
        files = item[2]
        break

    model_predict = tflearn.DNN(cnn(), tensorboard_verbose=0, checkpoint_path=None,
                        best_checkpoint_path=CHECK_POINT,
                        max_checkpoints=100, tensorboard_dir=LOG_PATH)
    model_predict.load('/Users/tairy/Documents/Working/python-lab/tensorflow/taobao_captcha')


    for i, filename in enumerate(files):
        if '.DS_Store' == filename:
            continue
        print('[+]加载图片:%s' % filename)
        predict_X = split_image(filename)
        result = model_predict.predict(predict_X)
        result_str = ''
        for i in range(result.shape[0]):
            predict = vec2text(result[i])
            result_str += predict
        os.renames('./test_set/' + filename, './test_set/' + result_str + '.jpeg')
        print('[+]预测结果:%s' % result_str)


def main():
    predict()
if __name__ == '__main__':
    main()
