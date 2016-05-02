#coding=utf-8
import codecs

def main():
    tags = codecs.open('../../data/tag_name.txt', 'r', encoding='UTF-8').readlines()
    bad_tags = codecs.open('../../data/bad_tags.txt', 'r', encoding='UTF-8').readlines()
    target_file = codecs.open('../../data/good_tags.txt', 'w+', encoding='UTF-8')

    for tag in tags:
        if(tag not in bad_tags):
            target_file.write(tag)
    print 'Success!'

if __name__ == '__main__':
    main()