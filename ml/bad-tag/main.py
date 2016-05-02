#coding=utf-8
import jieba
import codecs
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    tags = codecs.open('../../data/tag_name.txt', 'r', encoding='UTF-8').readlines()
    stop_words = codecs.open('../../data/black_list.txt', 'r', encoding='UTF-8').readlines()
    target_file = codecs.open('../../data/bad_tags.txt', 'w+', encoding='UTF-8')
    white_list = codecs.open('../../data/white_list.txt', 'r', encoding='UTF-8').readlines()

    for tag in tags:
        # tag = tag.strip('\n')
        # get repeat latter
        if tag not in white_list:
            tag_re = re.compile(ur'([0-9a-zA-Z])\1{2,}|([0-9]){4,}')
            if(tag_re.search(tag)):
                target_file.write(tag)
                continue
            chinese_re = re.compile(ur'([\u4e00-\u9fa5])\1{1,}')
            if(chinese_re.search(tag)):
                target_file.write(tag)
                continue

            # get stop list
            tag_words = jieba.cut(tag)
            for word in tag_words:
                if(word + '\n' in stop_words):
                    target_file.write(tag)
                    continue
if __name__ == '__main__':
    main()
