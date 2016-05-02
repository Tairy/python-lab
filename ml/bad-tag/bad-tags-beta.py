#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jieba
from numpy import *
import codecs

def levenshtein(source, dest):
    '''Return the levenshteiin distance between source and dest'''
    row_len = len(source) + 1
    col_len = len(dest) + 1

    if row_len == 1 or col_len == 1:
        return max(row_len, col_len)

    matrix = [[col+row for col in range(col_len)] for row in range(row_len)]

    for row in xrange(1, row_len):
        for col in xrange(1, col_len):
            cost = 0 if source[row - 1] == dest[col - 1] else 1

            deletion = matrix[row-1][col] + 1
            insertion = matrix[row][col-1] + 1
            substitution = matrix[row-1][col-1] + cost

            matrix[row][col] = min(deletion, insertion, substitution)

    return matrix[row_len-1][col_len-1]

if __name__ == '__main__':
    root_words = codecs.open("../data/root_words.txt", "r", encoding="UTF-8").readlines()
    target_words = codecs.open("../data/tag_name.txt", "r", encoding="UTF-8").readlines()
    # # map(encode, target_words)
    # print root_words
    for target_word in target_words:
        # for root_word in root_words:
        words = jieba.cut(target_word)
        for word in words:
            if(word + "\n" in root_words):
                print target_word.encode("utf-8")
            # print word.encode("utf-8")
            # if(word in )
            # if(target_word.find(root_word)):
            #     print target_word.encode("utf-8")
        # words = jieba.cut(target_word)
        # for word in words:

        #   # print word.encode("utf-8")
        # all_dis = 0
        # for root_word in root_words:
        #     str_max_len = max(len(target_word), len(root_word.strip("\n")))
        #     ld_dis = levenshtein(root_word.strip("\n"), target_word)
        #     if(ld_dis == str_max_len):
        #         all_dis += 0
        #     else:
        #         all_dis += ld_dis
        # if all_dis > 6:
        #   print target_word.encode("utf-8")
        #   print all_dis
