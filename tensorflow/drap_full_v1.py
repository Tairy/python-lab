# encoding:utf-8
import os
import cv2
import numpy as np
import argparse
from itertools import groupby
from os.path import basename


def get_projection_x(image):  # axis = 0: x轴, axis = 1: y轴
    # 初始化投影标记list
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
    # print(image.shape[:2])
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
    # print(end_route)
    # for r in end_route:
    #     image[r[1], r[0]] = [0, 0, 255]
    #
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    filter_end_route = [max(list(k)) for _, k in groupby(end_route, lambda x: x[1])]
    # 两个字符的图片，首先得到的是左边那个字符
    img1 = do_split(image, start_route, filter_end_route)
    border1 = get_black_border(img1)
    # 再得到最右边字符
    start_route = list(map(lambda x: (x[0] + 1, x[1]), filter_end_route))
    end_route = []
    for y in range(height):
        end_route.append((width - 1, y))

    img2 = do_split(image, start_route, end_route)
    border2 = get_black_border(img2)
    border2[0] += start_x
    border2[2] += start_x
    return [border1, border2]


def main():
    for item in os.walk('./predict_set'):
        files = item[2]
        break
    # files = ['9234.jpeg']
    for file in files:
        print("当前待切割图片:%s" % (file))
        img = cv2.imread('./predict_set/' + file)
        filename = file.split('.')[0]

        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
        split_image = cv2.cvtColor(split_image, cv2.COLOR_GRAY2BGR)
        # cv2.imwrite("splits/origin_split_image.jpeg", origin_split_image)
        # cv2.imwrite("splits/split_image.jpeg", split_image)

        for i in reversed(range(2, 7)):
            r_i = 6 - i
            # print(r_i)
            # print(filename[r_i])
            borders = drop_fall(split_image, i)
            # print(borders)
            child_img = origin_split_image[borders[0][1]:borders[0][3], borders[0][0]:borders[0][2]]
            child_img = cv2.resize(child_img, (20, 20), interpolation=cv2.INTER_CUBIC)
            # cv2.imwrite("predict_splits/" + filename + "-" + str(r_i) + "-" + filename[r_i] + ".jpeg", child_img)
            cv2.imwrite("predict_splits/" + filename + "-" + str(r_i) + "-" + str(r_i) + ".jpeg", child_img)

            # break
            split_image = split_image[borders[1][1]:borders[1][3], borders[1][0]:borders[1][2]]
            origin_split_image = origin_split_image[borders[1][1]:borders[1][3], borders[1][0]:borders[1][2]]
            # cv2.imwrite("splits/ss-" + filename + "-" + str(r_i) + "-" + filename[r_i] + ".jpeg", split_image)
            if 2 == i:
                if len(origin_split_image) > 0:
                    origin_split_image = cv2.resize(origin_split_image, (20, 20), interpolation=cv2.INTER_CUBIC)
                    # cv2.imwrite("predict_splits/" + filename + "-5-" + filename[5] + ".jpeg", origin_split_image)
                    cv2.imwrite("predict_splits/" + filename + "-5-5.jpeg", origin_split_image)
                    # cv2.imwrite("splits/child-" + str(i - 1) + ".jpeg", origin_split_image)

        print("切割完成:%s" % (file))


if __name__ == '__main__':
    main()
