# encoding:utf-8

import numpy as np
import tflearn
from tflearn.layers.core import input_data
import re
import os
from es import es
import collections

MODEL_NAME = "log_classify"


def get_tagged_logs():
    query_json = {
        "bool": {
            "must": [
                {
                    "exists": {"field": "tags"}
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

    res = es.search(index="app-server-log-prod-*", body={"query": query_json, "sort": sort_json, "size": 500})

    hits = res['hits']['hits']

    return hits


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
                    body={"query": query_json, "sort": sort_json, "size": 200},
                    request_timeout=500)

    hits = res['hits']['hits']

    return hits


def log_to_vec(action="train"):
    if action == "train":
        logs = get_tagged_logs()
    else:
        logs = get_origin_data()
    print("总共%d条", len(logs))
    dicts = [line.strip() for line in open("dict.txt", 'r')]
    dict_map = {}
    dict_len = len(dicts)
    for i, w in enumerate(dicts):
        dict_map[w] = i

    tags = [line.strip() for line in open("tags.txt", 'r')]
    tags_map = {}
    tags_len = len(tags)

    for i, t in enumerate(tags):
        tags_map[t] = i

    x_batch = np.zeros([len(logs), dict_len])
    y_batch = np.zeros([len(logs), tags_len])
    for idx, log in enumerate(logs):
        if action == 'train':
            tag = log['_source']['tags'][0]
            if tag not in tags_map:
                continue
            tag_vec = np.zeros(tags_len)
            tag_vec[tags_map[tag]] = 1
            y_batch[idx, :] = tag_vec
        word_vec = np.zeros(dict_len)
        words = re.findall("\w+", str.lower(log['_source']['em'].strip()))
        for word in words:
            word = word.lower()
            if word in dict_map:
                word_vec[dict_map[word]] = 1
        x_batch[idx, :] = word_vec

    return x_batch, y_batch, dict_len, tags_len, logs, tags


def batch_load_logs():
    dicts = [line.strip() for line in open("dict.txt", 'r')]
    dict_map = {}
    dict_len = len(dicts)
    for i, w in enumerate(dicts):
        dict_map[w] = i

    tags = [line.strip() for line in open("tags.txt", 'r')]
    tags_map = {}
    tags_len = len(tags)

    for i, t in enumerate(tags):
        tags_map[t] = i

    files = []
    for item in os.walk('./dataset'):
        files = item[2]
        break

    logs = []
    for i, filename in enumerate(files):
        tag = filename.split('.')[0]
        for line in open("./dataset/" + filename, 'r'):
            logs.append(line.strip() + "\t" + tag)

    log_count = len(logs)
    x_batch = np.zeros([log_count, dict_len])
    y_batch = np.zeros([log_count, tags_len])

    for idx, log in enumerate(logs):
        log_arr = log.split("\t")
        log_str = log_arr[0]
        log_tag = log_arr[1]
        word_vec = np.zeros(dict_len)
        words = re.findall("\w+", str.lower(log_str.strip()))
        for word in words:
            word = word.lower()
            if word in dict_map:
                word_vec[dict_map[word]] = 1
        tag_vec = np.zeros(tags_len)
        tag_vec[tags_map[log_tag]] = 1
        x_batch[idx, :] = word_vec
        y_batch[idx, :] = tag_vec

    return x_batch, y_batch, dict_len, tags_len


def cnn(dict_len, tags_len):
    network = input_data(shape=[None, dict_len], name='input')
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, tags_len, activation='softmax')
    network = tflearn.regression(network)
    return network


"""
构建日志词典
"""


def build_dict(min_word_freq=1):
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


"""
训练分类模型
"""


def train():
    # x_batch, y_batch, dict_len, tags_len, _, _ = log_to_vec('train')
    x_batch, y_batch, dict_len, tags_len = batch_load_logs()
    model = tflearn.DNN(cnn(dict_len, tags_len))
    model.fit(x_batch, y_batch, n_epoch=10, batch_size=16, show_metric=True)
    model.save("./model/" + MODEL_NAME)


"""
检查分类结果
"""


def predict():
    x_batch, y_batch, dict_len, tags_len, logs, tags = log_to_vec('predict')
    model_predict = tflearn.DNN(cnn(dict_len, tags_len))
    model_predict.load('/Users/tairy/Documents/Working/python-lab/log-classify/model/' + MODEL_NAME)
    result = model_predict.predict(x_batch)
    for i in range(result.shape[0]):
        print(logs[i]['_source']['em'])
        max_index = np.argmax(result[i])
        print('[+]预测结果:%s' % tags[max_index])
        print(">>>!<<<")


if __name__ == "__main__":
    build_dict(10)
    train()
    predict()
