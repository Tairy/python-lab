# encoding:utf-8

import cv2
import numpy as np
from itertools import groupby


class SplitImage(object):
    def preprocess(self, image):
        origin_image = image
        image = self._binaryzation(image)
        child_images = self._cut_images(image, origin_image)
        return child_images

    def _binaryzation(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
        return image

    def _show(self, image):
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def _cut_images(self, image, origin_image):
        split_seq = self._get_split_seq(self._get_projection_x(image))
        # print(split_seq)
        croped_images = []
        croped_origin_images = []
        height = image.shape[0]

        for start_x, width in split_seq:
            # 同时去掉y轴上下多余的空白
            begin_row = 0
            end_row = height - 1
            for row in range(height):
                flag = True
                for col in range(start_x, start_x + width):
                    if image[row, col] == 0:
                        flag = False
                        break
                if not flag:  # 如果在当前行找到了黑色像素点，就是起始行
                    begin_row = row
                    break
            for row in reversed(range(height)):
                flag = True
                for col in range(start_x, start_x + width):
                    if image[row, col] == 0:
                        flag = False
                        break
                if not flag:
                    end_row = row
                    break

            croped_origin_images.append(origin_image[begin_row:end_row + 1, start_x:start_x + width])
            croped_images.append(image[begin_row:end_row + 1, start_x:start_x + width])

        need_drop_fall = False
        for idx, split_info in enumerate(split_seq):
            if self._is_joint(split_info[1]):
                need_drop_fall = True
                print("找到一张粘连图片: %d" % idx)
                split_image_bolders = self._drop_fall(croped_images[idx])
                break
        if need_drop_fall:
            del croped_origin_images[idx]
            croped_origin_images.insert(idx, origin_image[split_image_bolders[0][1]:split_image_bolders[0][3],
                                      split_image_bolders[0][0]:split_image_bolders[0][2]])

            croped_origin_images.insert(idx + 1, origin_image[split_image_bolders[1][1]:split_image_bolders[1][3],
                                          split_image_bolders[1][0]:split_image_bolders[1][2]])

        return croped_origin_images

    def _drop_fall(self, image):
        """
        对粘连两个字符的图片进行drop fall算法分割
        """
        # 1. 竖直投影统计
        height, width = image.shape
        print("当前待切割图片的 width: %d, height: %d" % (width, height))
        hist_width = [0] * width
        for x in range(width):
            for y in range(height):
                if image[y, x] == 0:
                    hist_width[x] += 1
        # 2. 找到极小值点
        start_x = self._get_start_x(hist_width)

        # 3. 以这个极小值点作为起始滴落点,实施滴水算法
        start_route = []
        for y in range(height):
            start_route.append((0, y))

        end_route = self._get_end_route(image, start_x, height)
        filter_end_route = [max(list(k)) for _, k in groupby(end_route, lambda x: x[1])]
        # 两个字符的图片，首先得到的是左边那个字符
        img1 = self._do_split(image, start_route, filter_end_route)
        border1 = self._get_black_border(img1)
        # img1 = img1[border[1]:border[3], border[0]:border[2]]

        # 再得到最右边字符
        start_route = list(map(lambda x: (x[0] + 1, x[1]), filter_end_route))
        end_route = []
        for y in range(height):
            end_route.append((width - 1, y))

        img2 = self._do_split(image, start_route, end_route)
        border2 = self._get_black_border(img2)
        border2[0] += start_x
        border2[2] += start_x
        # border2 = list(map(lambda x: (start_x + x), border2))
        # img2 = img2[border[1]:border[3], border[0]:border[2]]

        return [border1, border2]

    def _get_black_border(self, image):
        """
        获取指定图像的内容边界坐标
        :param image: 图像 Image Object
        :return: 图像内容边界坐标tuple (left, top, right, bottom)
        """
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        height, width = image.shape
        max_x = max_y = 0
        min_x = width - 1
        min_y = height - 1
        for y in range(height):
            for x in range(width):
                if image[y, x] == 0:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        return [min_x, min_y, max_x + 1, max_y + 1]

    def _do_split(self, source_image, starts, filter_ends):
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
                if source_image[start[1], x] == 0:
                    image[start[1] - top, x - left] = [0, 0, 0]
                else:
                    image[start[1] - top, x - left] = [255, 255, 255]

        return image

    def _is_joint(self, split_len):
        """
        以字符宽度统计值判断当前split_len是否是两个字符的长度
        返回True需要进一步进行滴水算法分割
        """
        return True if split_len >= 18 else False

    def _get_end_route(self, image, start_x, height):
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
                curW = self._get_nearby_pixel_val(image, cur_p[0], cur_p[1], i) * (6 - i)
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

    def _get_nearby_pixel_val(self, image, cx, cy, j):
        if j == 1:
            return 0 if image[cy + 1, cx - 1] == 0 else 1
        elif j == 2:
            return 0 if image[cy + 1, cx] == 0 else 1
        elif j == 3:
            return 0 if image[cy + 1, cx + 1] == 0 else 1
        elif j == 4:
            return 0 if image[cy, cx + 1] == 0 else 1
        elif j == 5:
            return 0 if image[cy, cx - 1] == 0 else 1
        else:
            raise Exception("what you request is out of nearby range")

    def _get_start_x(self, hist_width):
        """
        根据待切割的图片的竖直投影统计hist_width，找到合适的滴水起始点
        hist_width的中间值，前后再取4个值，在这个范围内找最小值
        """
        mid = int(len(hist_width) / 2)
        # 共9个值
        return mid - 4 + np.argmin(hist_width[mid - 4:mid + 5])

    # 获取切割后的x轴坐标点，返回值为[初始位置，长度]的列表
    def _get_split_seq(self, projection_x):
        split_seq = []
        start_x = 0
        length = 0
        for pos_x, val in enumerate(projection_x):
            if val == 0 and length == 0:
                continue
            elif val == 0 and length != 0:
                split_seq.append([start_x, length])
                length = 0
            elif val == 1:
                if length == 0:
                    start_x = pos_x
                length += 1
            else:
                raise Exception('generating split sequence occurs error')
        # 循环结束时如果length不为0，说明还有一部分需要append
        if length != 0:
            split_seq.append([start_x, length])
        return split_seq

    # 图片到x轴或y轴的投影，如果有数据（黑色像素点）值为1，否则为0
    def _get_projection_x(self, image):  # axis = 0: x轴, axis = 1: y轴
        # 初始化投影标记list
        height, width = image.shape
        p_x = [0 for _ in range(width)]

        for x in range(width):
            for y in range(height):
                if image[y, x] == 0:
                    p_x[x] = 1
                    break
        return p_x


def main():
    captcha = SplitImage()
    image = cv2.imread('./train_set/000340.jpeg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    child_images = captcha.preprocess(image)
    for i, img in enumerate(child_images):
        # image_count += 1
        # captcha.preprocess(img)
        cv2.imwrite("splits/child-" + str(i) + ".jpg", img)
    # while image_count < 6:
    #     child_images = captcha.preprocess(image)
    #     for i, img in enumerate(child_images):
    #         image_count += 1
    #         captcha.preprocess(img)
    #         # cv2.imwrite("splits/child-" + str(i) + ".jpg", img)


if __name__ == '__main__':
    main()
