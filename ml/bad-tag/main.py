#coding=utf-8
import jieba
import codecs
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    tags = codecs.open('../../data/tag_name_and_id.txt', 'r', encoding='UTF-8').readlines()
    stop_words = codecs.open('../../data/black_list.txt', 'r', encoding='UTF-8').readlines()
    white_list = codecs.open('../../data/white_list.txt', 'r', encoding='UTF-8').readlines()
    patterns = codecs.open('../../data/bad_pattern.txt', 'r', encoding='UTF-8').readlines()
    bad_tags = codecs.open('../../data/bad_tags.txt', 'w+', encoding='UTF-8')
    good_tags = codecs.open('../../data/good_tags.txt', 'w+', encoding='UTF-8')
    bad_tag_ids = codecs.open('../../data/bad_tag_ids.txt', 'w+', encoding='UTF-8')

    for tag in tags:
        # get repeat latter
        split_tag = tag.split()
        tag_id = split_tag[0]
        tag = split_tag[1]
        if tag not in white_list:
            word_flag = re_flag = False
            for pattern in patterns:
                pattern = pattern.strip('\n')
                pattern = eval('ur"' + pattern + '"')
                tag_re = re.compile(pattern)
                if(tag_re.search(tag)):
                    re_flag = True

            # get stop list
            tag_words = jieba.cut(tag)
            for word in tag_words:
                if(word + '\n' in stop_words or tag + '\n' in stop_words):
                    word_flag = True
            if re_flag or word_flag:
                bad_tags.write(tag + '\n')
                bad_tag_ids.write(tag_id + '\n')
                continue

        good_tags.write(tag + '\n')



if __name__ == '__main__':
    main()
