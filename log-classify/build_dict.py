# encoding:utf-8
import collections
import re
import os
from es import es


def get_origin_data():
    query_json = {
        "bool": {
            "must": [
                {
                    "match": {
                        "an": "sqkb-api-v2"
                    }
                },
                {
                    "match": {
                        "ll": "ERROR"
                    }
                }
            ]
        }
    }

    sort_json = [
        {
            "dt": {
                "order": "desc"
            }
        }
    ]

    res = es.search(index="app-server-log-prod-*",
                    body={"query": query_json, "sort": sort_json, "size": 5000},
                    request_timeout=500)

    hits = res['hits']['hits']

    return hits


def build_dict_v2(min_word_freq=1):
    files = []
    for item in os.walk('./dataset'):
        files = item[2]
        break
    word_freq = collections.defaultdict(int)
    dict_file = open("dict.txt", "a")
    for i, filename in enumerate(files):
        logs = [line.strip() for line in open("./dataset/" + filename, 'r')]
        for log in logs:
            words = re.findall("\w+", str.lower(log.strip()))
            for word in words:
                if word.isalpha():
                    word_freq[word] += 1
    word_freq = filter(lambda x: x[1] > min_word_freq, word_freq.items())
    word_freq_sorted = sorted(word_freq, key=lambda x: (-x[1], x[0]))
    word_dicts, _ = list(zip(*word_freq_sorted))
    dict_content = ''
    for w in word_dicts:
        dict_content += w + "\n"

    dict_file.write(dict_content)
    dict_file.close()


def build_dict(min_word_freq=1):
    word_freq = collections.defaultdict(int)
    logs = get_origin_data()
    dict_file = open("dict.txt", "a")
    for log in logs:
        words = re.findall("\w+", str.lower(log['_source']['em'].strip()))
        for word in words:
            if word.isalpha():
                word_freq[word] += 1

    word_freq = filter(lambda x: x[1] > min_word_freq, word_freq.items())
    word_freq_sorted = sorted(word_freq, key=lambda x: (-x[1], x[0]))
    word_dicts, _ = list(zip(*word_freq_sorted))
    dict_content = ''
    for w in word_dicts:
        dict_content += w + "\n"

    dict_file.write(dict_content)
    dict_file.close()


if __name__ == "__main__":
    build_dict_v2(10)
