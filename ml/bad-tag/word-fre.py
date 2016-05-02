#coding=utf-8
import jieba
import codecs

file = codecs.open("../../data/2_bad_tags.txt", "r", encoding="UTF-8")
target_file = codecs.open("../../data/3_word_fre_sorted.txt", "w+", encoding="UTF-8")
stop_words = codecs.open("../../data/1_stop_words.txt", "r", encoding="UTF-8").readlines()
white_words = codecs.open("../../data/1_wihte_list.txt", "r", encoding="UTF-8").readlines()
# print stop_words
word_fre = {}

for line in file.readlines():
    words = jieba.cut(line)
    for word in words:
        word = word.strip()
        if not word_fre.has_key(word):
            word_fre[word] = 1
        word_fre[word] += 1

word_fre = sorted(word_fre.iteritems(), key = lambda d:d[1], reverse = True)
# print word_fre
for i in word_fre:
    # print i[0].encode("utf-8")
    write_word = i[0] + "\n"
    if(write_word not in stop_words and write_word not in white_words):
        target_file.write (write_word)

print "Success!"
