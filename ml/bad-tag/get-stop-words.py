#coding=utf-8
import jieba
import codecs

file = codecs.open("../data/tag_name.txt", "r", encoding="UTF-8")
target_file = codecs.open("../data/word_fre_sorted", "w+", encoding="UTF-8")