# encoding:utf-8
from elasticsearch import Elasticsearch
import collections

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


def build_dict(min_word_freq=1):
    word_freq = collections.defaultdict(int)
    logs = get_origin_data()
    dict_file = open("dict.txt", "a")
    for log in logs:
        for word in log['_source']['em'].strip().split():
            # if word.isalpha():
            word_freq[word] += 1

    word_freq = filter(lambda x: x[1] > min_word_freq, word_freq.items())
    word_freq_sorted = sorted(word_freq, key=lambda x: (-x[1], x[0]))
    words, _ = list(zip(*word_freq_sorted))
    dict_content = ''
    for word in words:
        dict_content += word + "\n"

    dict_file.write(dict_content)
    dict_file.close()


if __name__ == "__main__":
    build_dict(1)
